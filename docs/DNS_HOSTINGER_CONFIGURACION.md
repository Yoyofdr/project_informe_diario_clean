# Configuración DNS en Hostinger para GitHub Pages

## 📋 Registros DNS necesarios

### Para el dominio principal (informediariochile.cl):

**Registro 1:**
- Type: `A`
- Name: `@` (o déjalo vacío)
- Points to: `185.199.108.153`
- TTL: `14400` (o default)

**Registro 2:**
- Type: `A`
- Name: `@` (o déjalo vacío)
- Points to: `185.199.109.153`
- TTL: `14400` (o default)

**Registro 3:**
- Type: `A`
- Name: `@` (o déjalo vacío)
- Points to: `185.199.110.153`
- TTL: `14400` (o default)

**Registro 4:**
- Type: `A`
- Name: `@` (o déjalo vacío)
- Points to: `185.199.111.153`
- TTL: `14400` (o default)

### Para www.informediariochile.cl:

**Registro 5:**
- Type: `A`
- Name: `www`
- Points to: `185.199.108.153`
- TTL: `14400` (o default)

**Registro 6:**
- Type: `A`
- Name: `www`
- Points to: `185.199.109.153`
- TTL: `14400` (o default)

**Registro 7:**
- Type: `A`
- Name: `www`
- Points to: `185.199.110.153`
- TTL: `14400` (o default)

**Registro 8:**
- Type: `A`
- Name: `www`
- Points to: `185.199.111.153`
- TTL: `14400` (o default)

## ⚠️ Importante

1. **NO uses CNAME** para www si ya tienes registros A
2. **Elimina** cualquier registro conflictivo antes de agregar los nuevos
3. Si ves un registro como "parked" o "default", elimínalo

## 🔍 Verificación

Después de guardar, verifica con:
```bash
nslookup informediariochile.cl
nslookup www.informediariochile.cl
```

Ambos deben mostrar las 4 IPs de GitHub.

## 🚨 Si sigues teniendo problemas:

1. **Revisa si hay registros MX o TXT** que puedan estar en conflicto
2. **Contacta soporte de Hostinger** - pueden tener restricciones específicas
3. **Alternativa**: Usa solo registros A para @ y configura una redirección de www a @ en Hostinger