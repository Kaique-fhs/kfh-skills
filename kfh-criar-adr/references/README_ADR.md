# ADRs (Architecture Decision Records)

## Sobre

Este diretório contém os ADRs (Architecture Decision Records) do projeto.

ADRs registram decisões importantes de arquitetura, incluindo contexto, decisão e impactos.

---

## Quando criar um ADR

Crie um ADR quando:

- houver uma decisão arquitetural relevante  
- existir trade-off (ganho vs perda)  
- impactar comportamento do sistema  
- envolver risco, IA ou regras de negócio  

---

## Template

Todos os ADRs devem seguir o padrão definido em:

`TEMPLATE_ADR.md`

Os campos `Emendada por`, `Adendo` e `Errata` são opcionais — ver
`TEMPLATE_ADR.md` para o formato.

---

## Estrutura

- Local: `docs/ams/adr/`
- Nome dos arquivos: `ADR-XXX-frase-verbal-imperativa.md`
- Numeração sequencial (ADR-001, ADR-002, ...)
- A parte textual do nome do arquivo deve usar, quando praticável, uma
  frase verbal imperativa no presente (ex.: `centralizar-o-escopo-de-...`).
  ADRs existentes não são renomeadas só por causa desta regra — renomear
  muda a URL de toda referência cruzada (specs, planos, outras ADRs que
  citam pelo nome do arquivo). Renomeie apenas quando o número do arquivo
  mudar por outro motivo (ex.: renumeração por colisão).
- O nome do arquivo deve usar apenas minúsculas e traços
- A série `ADR-LOCAL-*` foi aposentada junto com a Mitra (ADR-009). Todo ADR é `ADR-NNN`

Exemplo:

- `ADR-001-adotar-fluxo-de-analise-antes-da-implementacao.md`

---

## Regras

- ADR deve ser curto e direto  
- A decisão deve ser clara e sem ambiguidade  
- Sempre explicitar consequências (impactos)  
- O nome da ADR deve ser legível, acionável e compatível com a convenção de nomes do repositório  

---

## Objetivo

- Manter histórico de decisões  
- Facilitar entendimento do sistema  
- Evitar rediscussões desnecessárias  
- Garantir consistência arquitetural
