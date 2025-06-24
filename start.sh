#!/bin/bash

echo "Ejecutando script R..."
Rscript descargar_datos.R

echo "Iniciando servidor HTTP en puerto 8080..."
python3 -m http.server 8080
