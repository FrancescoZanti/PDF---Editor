# Tema Chiaro/Scuro Automatico

## Descrizione
PDF Editor supporta ora il rilevamento automatico del tema di sistema di Windows 10/11. L'applicazione si adatta automaticamente al tema chiaro o scuro configurato nel sistema operativo.

## Funzionamento Automatico
Al primo avvio, l'applicazione:
1. Rileva il tema di sistema di Windows
2. Applica automaticamente il tema corrispondente (chiaro o scuro)
3. Salva la preferenza come "auto" nel file di configurazione

## Modalità Disponibili
L'applicazione supporta tre modalità di tema:
- **auto** (predefinito): Si adatta automaticamente al tema di Windows
- **light**: Forza il tema chiaro indipendentemente dalle impostazioni di sistema
- **dark**: Forza il tema scuro indipendentemente dalle impostazioni di sistema

## Cambiare Manualmente il Tema
Per cambiare manualmente il tema, modifica il file di configurazione:

**Percorso:** `C:\Users\[TuoNomeUtente]\.pdf_editor_pro\config.json`

**Esempio:**
```json
{
    "theme": "auto",
    ...
}
```

Cambia il valore di `"theme"` in:
- `"auto"` per il rilevamento automatico
- `"light"` per il tema chiaro fisso
- `"dark"` per il tema scuro fisso

## Rilevamento del Tema di Windows
Su Windows 10/11, il tema viene rilevato leggendo la chiave di registro:
```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize
Valore: AppsUseLightTheme
```
- Valore `1` = Tema chiaro
- Valore `0` = Tema scuro

## Tema Chiaro
Il tema chiaro utilizza:
- Sfondo principale: #f5f5f5 (grigio chiaro)
- Pannelli: bianco (#ffffff)
- Testo: #2c3e50 (grigio scuro)
- Bordi: #e0e0e0 (grigio)

## Tema Scuro
Il tema scuro utilizza:
- Sfondo principale: #1e1e1e (grigio molto scuro)
- Pannelli: #2d2d2d (grigio scuro)
- Testo: #e0e0e0 (grigio chiaro)
- Bordi: #3a3a3a (grigio medio)

## Compatibilità
- ✅ Windows 10
- ✅ Windows 11
- ⚠️ Altri sistemi operativi: usa il tema chiaro come predefinito

## Note Tecniche
- Il tema viene applicato all'avvio dell'applicazione
- Per vedere le modifiche dopo aver cambiato il tema di Windows, riavvia l'applicazione
- I pulsanti mantengono i loro colori distintivi in entrambi i temi
- L'area di visualizzazione PDF si adatta al tema per una migliore leggibilità

## Risoluzione Problemi

### Il tema non si aggiorna automaticamente
- Soluzione: Riavvia l'applicazione dopo aver cambiato il tema di Windows

### Il tema è sempre chiaro anche con Windows in modalità scura
- Verifica che il tema nelle impostazioni del config.json sia "auto"
- Assicurati che le impostazioni di Windows siano corrette:
  - Impostazioni → Personalizzazione → Colori → "Scegli la modalità"

### Preferisco sempre lo stesso tema indipendentemente da Windows
- Modifica il config.json e imposta `"theme": "light"` o `"theme": "dark"`
