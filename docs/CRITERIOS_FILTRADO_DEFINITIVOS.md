# 📋 CRITERIOS DE FILTRADO DEFINITIVOS - INFORME DIARIO

## 🎯 RESUMEN EJECUTIVO

El sistema de filtrado profesional para hechos esenciales CMF se basa en las mejores prácticas de Bloomberg/Refinitiv, diseñado para identificar y priorizar información relevante para inversionistas institucionales.

### 🔑 Reglas Fundamentales
- **Máximo 12 hechos por informe** (NUNCA más)
- **Regla Dorada**: "¿Le importaría esto a un inversionista institucional?"
- **Priorización por relevancia calculada** (escala 1-10)

---

## 📊 CATEGORÍAS DE RELEVANCIA

### 🔴 CRÍTICOS (9-10 puntos)
**Siempre incluir - Sin excepciones**

**Palabras clave detectadas:**
- Cambios de control: OPA, toma de control, venta de control
- M&A: fusión, adquisición, merger, spin-off, escisión
- Profit warnings: advertencia de resultados, deterioro significativo
- Crisis financiera: quiebra, insolvencia, default, reestructuración de deuda

### 🟡 IMPORTANTES (7-8.9 puntos)
**Incluir si hay espacio disponible**

**Palabras clave detectadas:**
- Alta gerencia: cambio/renuncia CEO, CFO, Gerente General
- Emisiones: bonos, acciones, aumento de capital
- Contratos materiales: adjudicación, joint venture, alianza estratégica
- Inversiones significativas: nueva planta, expansión

### 🟢 MODERADOS (5-6.9 puntos)
**Incluir solo si hay espacio después de críticos e importantes**

**Palabras clave detectadas:**
- Resultados: FECU, estados financieros trimestrales
- Juntas: citación, junta extraordinaria
- Dividendos: reparto de utilidades, política de dividendos
- Cambios menores: director, ejecutivo, estatutos

### ⚪ RUTINARIOS (<5 puntos)
**NUNCA incluir - Descartados automáticamente**

**Palabras clave detectadas:**
- Administrativos: cambio domicilio, certificados
- Correcciones: fe de erratas, rectificación, aclaración

---

## 🏢 BONIFICACIÓN POR EMPRESA

### Empresas IPSA (+2.5 puntos)
Empresas del índice bursátil principal de Chile:
- **Bancos**: Banco de Chile, Santander, BCI, Itaú
- **Retail**: Cencosud, Falabella, Ripley, SMU
- **Utilities**: Enel Chile, Colbún, Aguas Andinas
- **Commodities**: SQM, COPEC, CMPC, CAP
- **Otros**: CCU, Concha y Toro, Parque Arauco

### Empresas Estratégicas (+0.8 puntos)
Empresas relevantes no-IPSA:
- **Aerolíneas**: LATAM, Sky Airline
- **AFPs**: Habitat, Cuprum, Provida
- **Holdings**: Consorcio Financiero, Grupo Security
- **Salud**: Clínica Las Condes, RedSalud
- **Otros sectores clave**

---

## 🔧 PROCESO DE FILTRADO

### 1. Evaluación Inicial
```
Para cada hecho:
1. Detectar palabras clave → Asignar categoría
2. Verificar si es empresa IPSA/Estratégica
3. Calcular puntuación base + bonificaciones
```

### 2. Puntuación Final
```
Relevancia = Peso Base + Bonus Empresa + Factores Contexto

Donde:
- Peso Base: según categoría (2-9 puntos)
- Bonus IPSA: +2.5 puntos
- Bonus Estratégica: +0.8 puntos
- Contexto: +0.5 por montos USD significativos
- Contexto: +0.5 por impacto >10% en resultados
```

### 3. Selección Final
```
1. Ordenar todos los hechos por relevancia
2. Incluir TODOS los críticos (9-10)
3. Llenar espacios con importantes (7-8.9)
4. Completar con moderados (5-6.9) si hay espacio
5. DESCARTAR rutinarios (<5)
6. Límite estricto: 12 hechos máximo
```

---

## 📈 FACTORES ADICIONALES

### Bonificación por Contexto
- **Montos significativos en USD**: +0.5 puntos
- **Impacto en EBITDA/utilidad >10%**: +0.5 puntos
- **Operaciones internacionales**: consideración especial

### Consideraciones Especiales
- **Post-reestructuración**: Mayor sensibilidad (ej: LATAM)
- **Sectores regulados**: AFPs, Bancos, Utilities
- **Emisores frecuentes de bonos**: Metro, EFE, Codelco

---

## 🎯 REGLA DORADA APLICADA

Un hecho es relevante para un inversionista institucional si:

1. **Impacta valorización**: M&A, cambios de control, profit warnings
2. **Afecta gobierno corporativo**: Cambios CEO/CFO, directorio
3. **Modifica estructura financiera**: Emisiones, reestructuraciones
4. **Genera obligaciones materiales**: Contratos significativos
5. **Es de empresa IPSA**: Mayor liquidez y exposición de portafolio

---

## 📊 EJEMPLO DE APLICACIÓN

**Caso**: "CENCOSUD S.A. - Colocación de bonos por USD 500 millones"

1. **Detección**: "colocación de bonos" → Categoría IMPORTANTE
2. **Peso base**: 7.5 puntos
3. **Bonus IPSA**: +2.5 puntos (Cencosud ∈ IPSA)
4. **Contexto USD**: +0.5 puntos
5. **Relevancia final**: 10 puntos (capped) → 🔴 CRÍTICO

**Resultado**: Incluido con máxima prioridad

---

## 🚫 HECHOS DESCARTADOS (Ejemplos)

- "Cambio de domicilio social"
- "Fe de erratas en publicación anterior"
- "Certificado de inscripción en registro"
- "Actualización de datos de contacto"
- "Complemento de información previamente enviada"

---

## 📝 NOTAS IMPORTANTES

1. **Actualización semestral**: Revisar lista IPSA según cambios del índice
2. **Monitoreo continuo**: Ajustar keywords según evolución del mercado
3. **Feedback loop**: Incorporar retroalimentación de usuarios profesionales
4. **Transparencia**: Log detallado del proceso de filtrado en cada ejecución

---

## 🔄 ACTUALIZACIONES RECIENTES

- **2025-07**: Aumentado bonus IPSA de 1.5 a 2.5 puntos
- **2025-07**: Incluidos todos los moderados (no solo IPSA) si hay espacio
- **2025-07**: Agregadas keywords sin tilde para mejor detección
- **2025-07**: Implementada regla estricta de máximo 12 hechos

---

*Documento generado el 26 de julio de 2025*
*Basado en archivo: alerts/cmf_criterios_profesionales.py*