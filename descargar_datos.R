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
  
  write.zoo(eurusd, file = "./eurusd.csv", sep = ",", col.names = NA)
  write.zoo(vix, file = "./vix.csv", sep = ",", col.names = NA)
  write.zoo(dxy, file = "./dxy.csv", sep = ",", col.names = NA)
  
  cat("Descarga completada con éxito\n")
}, error = function(e) {
  cat("¡Error durante la ejecución del script R!\n")
  cat(e$message, "\n")
})

cat("Archivos generados en: ", getwd(), "\n")

