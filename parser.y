%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int yylex(void);
void yyerror(const char *s);

/* Cadena de entrada y posición */
static const char *input_str;
static int input_pos;
%}

%token TOK_A TOK_B
%start S

%%

S
    : TOK_A TOK_B
        { /* a b — caso base */ }
    | TOK_A S TOK_B
        { /* a^n S b^n */ }
    ;

%%

/* ── Lexer manual ── */
int yylex(void) {
    char c = input_str[input_pos];
    if (c == '\0') return 0;        /* EOF */
    input_pos++;
    if (c == 'a') return TOK_A;
    if (c == 'b') return TOK_B;
    return -1;                      /* token desconocido */
}

void yyerror(const char *s) {
    /* silenciamos el error para el benchmark */
    (void)s;
}

/* ── Función de parseo para una palabra ── */
extern int yyparse(void);

int bison_parse(const char *word) {
    input_str = word;
    input_pos = 0;
    return (yyparse() == 0);        /* 0 = éxito */
}

/* ── Benchmark ── */
int main(void) {
    /* Palabras de prueba: a^n b^n para n=1..17 */
    int max_n = 17;
    printf("%-6s %-36s %-8s %-14s\n",
           "n", "palabra (primeros 34 chars)", "acepta", "tiempo (ms)");
    printf("%s\n", "--------------------------------------------------------------");

    for (int n = 1; n <= max_n; n++) {
        /* construir a^n b^n */
        char *word = malloc(2 * n + 1);
        memset(word,       'a', n);
        memset(word + n,   'b', n);
        word[2 * n] = '\0';

        int REPS = 50000;
        int accepted = 0;

        struct timespec t0, t1;
        clock_gettime(CLOCK_MONOTONIC, &t0);
        for (int r = 0; r < REPS; r++) {
            accepted = bison_parse(word);
        }
        clock_gettime(CLOCK_MONOTONIC, &t1);

        double ms = ((t1.tv_sec - t0.tv_sec) * 1e9
                   + (t1.tv_nsec - t0.tv_nsec)) / 1e6 / REPS;

        /* mostrar solo primeros 34 chars */
        char preview[35];
        strncpy(preview, word, 34);
        preview[34] = '\0';

        printf("%-6d %-36s %-8s %.6f\n",
               n, preview, accepted ? "SI" : "NO", ms);
        free(word);
    }
    return 0;
}
