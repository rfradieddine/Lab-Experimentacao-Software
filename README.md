# LAB01 — Sprint 3 · Análise dos Gráficos e Validação das Hipóteses

---

## Sumário
- [RQ01 — Maturidade dos sistemas](#rq01--maturidade-dos-sistemas)
- [RQ02 — Contribuição externa (Pull Requests)](#rq02--contribuição-externa-pull-requests)
- [RQ03 — Releases](#rq03--releases)
- [RQ04 — Atualizações](#rq04--atualizações)
- [RQ05 — Linguagens utilizadas](#rq05--linguagens-utilizadas)
- [RQ06 — Issues fechadas](#rq06--issues-fechadas)
- [RQ07 — Comparação por linguagem](#rq07--comparação-por-linguagem)
- [Síntese das hipóteses](#síntese-das-hipóteses)
- [Limitações e próximos passos](#limitações-e-próximos-passos)

---

## RQ01 — Maturidade dos sistemas
**Pergunta:** Repositórios mais populares tendem a ser mais antigos?  
**Hipótese (S2):** Repositórios populares são, em geral, mais antigos, pois tiveram mais tempo para acumular estrelas e consolidar comunidade.

![RQ01 — Maturidade dos sistemas](LAB01%20-%20SPRINT%2001/RQ01_maturidade.png)

**Interpretação:** Visualmente, observa-se uma concentração em faixas intermediárias de idade, com poucos projetos extremamente novos ou extremamente antigos. Esse padrão **sugere uma vantagem para repositórios que já passaram dos estágios iniciais** (tempo suficiente para atrair usuários), mas **não implica que “quanto mais antigo, melhor”**: há casos recentes com alta tração.  
**Conclusão provisória:** *Hipótese parcialmente confirmada.* A maturidade ajuda, mas não é o único fator, projetos recentes com forte apelo também podem se tornar populares rapidamente.

---

## RQ02 — Contribuição externa (Pull Requests)
**Pergunta:** Repositórios populares recebem muitas contribuições externas?  
**Hipótese (S2):** Projetos populares apresentam grande volume (e aceitação) de PRs externos, pois a comunidade é maior.

![RQ02 — Contribuição externa](LAB01%20-%20SPRINT%2001/RQ02_contribuicao.png)

**Interpretação:** A distribuição parece **assimétrica**: poucos projetos concentram grande volume de PRs enquanto a maioria recebe quantidades modestas. Isso é típico de ecossistemas “long tail”. O volume de PRs tende a acompanhar a popularidade, mas **não de forma uniforme**; fatores como governança, documentação e rotinas de revisão influenciam fortemente.  
**Conclusão provisória:** *Hipótese parcialmente confirmada.* Popularidade ajuda, mas práticas de colaboração determinam quão efetivamente esse potencial vira PRs aceitos.

---

## RQ03 — Releases
**Pergunta:** Sistemas populares publicam releases com frequência?  
**Hipótese (S2):** Projetos populares mantêm **releases frequentes**, sinalizando manutenção contínua e preocupação com versões estáveis.

![RQ03 — Releases](LAB01%20-%20SPRINT%2001/RQ03_releases.png)

**Interpretação:** Nota-se **heterogeneidade**: alguns projetos mantêm cadência clara de releases, enquanto muitos publicam poucas (ou mesmo não utilizam “Releases” formais do GitHub). Em comunidades ativas, releases tendem a ser mais regulares; em bibliotecas/serviços estáveis, o número pode ser baixo sem indicar abandono.  
**Conclusão provisória:** *Hipótese apenas parcialmente confirmada.* Popularidade está associada à presença de releases em parcela dos projetos, mas **o rito formal de releases não é universal**.

---

## RQ04 — Atualizações
**Pergunta:** Projetos populares são atualizados com regularidade?  
**Hipótese (S2):** Sistemas populares mantêm **atividade recente** (commits, merges), acompanhando demandas e correções.

![RQ04 — Atualizações](LAB01%20-%20SPRINT%2001/RQ04_atualizacoes.png)

**Interpretação:** Os gráficos indicam **atividade recente em boa parte dos projetos**, com uma minoria visivelmente estagnada. Isso é consistente com a expectativa de que projetos mais usados mantêm ritmo de manutenção, embora **nem todo projeto popular tenha necessidade de atualizações frequentes** (p. ex., ferramentas estáveis).  
**Conclusão provisória:** *Hipótese confirmada em linhas gerais.* Popularidade costuma vir acompanhada de atividade, ainda que com diferentes cadências.

---

## RQ05 — Linguagens utilizadas
**Pergunta:** Quais linguagens predominam entre os repositórios populares?  
**Hipótese (S2):** A maioria utiliza linguagens amplamente difundidas (JavaScript/TypeScript, Python, Java etc.).

![RQ05 — Linguagens (distribuição por projeto)](LAB01%20-%20SPRINT%2001/RQ05_linguagens.png)
![Top 10 linguagens](LAB01%20-%20SPRINT%2001/top10_linguagens.png)

**Interpretação:** Observa-se **predominância de linguagens mainstream**, especialmente do ecossistema web e de ciência de dados/automação. Linguagens com comunidades grandes tendem a atrair mais contribuidores, documentação e ferramentas — reforçando o ciclo de popularidade.  
**Conclusão provisória:** *Hipótese confirmada.* As linguagens mais difundidas dominam entre os projetos populares analisados.

---

## RQ06 — Issues fechadas
**Pergunta:** Repositórios populares têm taxa alta de fechamento de issues?  
**Hipótese (S2):** Projetos populares **fecham issues com eficiência**, refletindo bom gerenciamento de comunidade.

![RQ06 — Issues fechadas](LAB01%20-%20SPRINT%2001/RQ06_issues.png)

**Interpretação:** O padrão visual sugere **dispersão**: há projetos com alto volume e boa taxa de fechamento e outros com backlog acumulado. Popularidade traz mais issues **e** mais atenção — o saldo depende da capacidade do time manter triagem/priorização.  
**Conclusão provisória:** *Hipótese parcialmente confirmada.* Repositórios populares **podem** ter boas taxas, mas a governança pesa mais que a popularidade por si só.

---

## RQ07 — Comparação por linguagem
**Pergunta:** Linguagens populares apresentam maior tração de comunidade e cadência de releases/atualizações?  
**Hipótese (S2):** Projetos em linguagens populares (Python, JS/TS etc.) **recebem mais PRs**, **lançam releases com maior frequência** e **têm ciclos de atualização menores**.

![RQ07 — Comparação por linguagem](LAB01%20-%20SPRINT%2001/RQ07_comparacao_linguagens.png)

**Interpretação:** A comparação entre linguagens aponta **vantagem consistente das linguagens mainstream** em métricas de engajamento (PRs, atividade) e operacionalização (releases), com destaque para ecossistemas com tooling e cultura de colaboração fortes. Linguagens de nicho exibem valores menores, porém **muitas vezes com cadência estável e alta qualidade**.  
**Conclusão provisória:** *Hipótese confirmada em linhas gerais.* A adoção massiva da linguagem costuma alavancar os indicadores de colaboração.

---

## Síntese das hipóteses

| RQ | Hipótese (Sprint 2) | Resultado na Sprint 3 |
|---|---|---|
| RQ01 | Popularidade correlaciona com sistemas mais antigos | **Parcialmente confirmada** |
| RQ02 | Popularidade → muitos PRs externos aceitos | **Parcialmente confirmada** |
| RQ03 | Populares lançam releases com frequência | **Parcialmente confirmada** |
| RQ04 | Populares são atualizados regularmente | **Confirmada (em geral)** |
| RQ05 | Predomínio de JS/TS, Python, Java… | **Confirmada** |
| RQ06 | Alta taxa de fechamento de issues | **Parcialmente confirmada** |
| RQ07 | Linguagens mainstream > melhor tração/cadência | **Confirmada (em geral)** |

