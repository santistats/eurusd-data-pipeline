cat("Iniciando descarga desde R...\n")

tryCatch({
  library(quantmod)
  library(tidyquant)
  library(conflicted)
  
  rm(list = ls())  # Limpia entorno
  options("getSymbols.warning4.0"=FALSE)
  
  symbol_eur = "EURUSD=X"
  symbol_vix = "^VIX"
  symbol_dxy = "DX-Y.NYB"
  start_date = as.Date("2008-01-01")
  end_date = Sys.Date()
  
  eurusd = getSymbols(symbol_eur, src = "yahoo", from = start_date, 
                      to = end_date, auto.assign = FALSE)
  vix = getSymbols(symbol_vix, src = "yahoo", from = start_date, 
                   to = end_date, auto.assign = FALSE)
  dxy = getSymbols(symbol_dxy, src = "yahoo", from = start_date, 
                   to = end_date, auto.assign = FALSE)
  
  # Ruta base
  ruta_base = "C:\\Users\\Usuario\\Desktop\\Universidad\\Tesis\\Database - my proyect"
  
  # Guardar archivos en esa ruta
  write.zoo(eurusd, file = file.path(ruta_base, "eurusd.csv"), sep = ",")
  write.zoo(vix,    file = file.path(ruta_base, "vix.csv"), sep = ",")
  write.zoo(dxy,    file = file.path(ruta_base, "dxy.csv"), sep = ",")
  
  cat("Descarga completada con éxito\n")
}, error = function(e) {
  cat("¡Error durante la ejecución del script R!\n")
  cat(e$message, "\n")
})

cat("Archivos generados en: ", getwd(), "\n")

