# Datos de la síntesis documental

`coafina-editions-public.csv` conserva una fila por edición, fechas, recuentos con unidad, fuentes y notas. ND significa no documentado; campos vacíos de 2026 corresponden a una actividad futura. `registered` puede ser aproximado o abierto; `participated` no equivale automáticamente a finalizar. `solutions_or_teams` conserva la unidad y no debe sumarse entre formatos.

`participation-flows.csv` contiene los renglones del cuadro de cocientes: numerador, denominador, umbral, cálculo y condiciones. 19/45=42,2%; 13/49=26,5%; la mitad es aproximada; 78/N con N>100 solo da <78% bajo equivalencia de cohorte. No se calcula una media combinada.

`evidence.csv` mantiene afirmaciones verificadas, atribuidas o pendientes. `source-preservation.json` registra fuentes fechadas y corroboraciones parciales. Los CSV son extracción documental, no microdatos ni sustitutos de formularios originales.

Los campos `opening_announced_*` conservan las cifras anunciadas en la apertura de 2025. Se mantienen separados de `participated`, que permanece ND por falta de un recuento final verificado.
