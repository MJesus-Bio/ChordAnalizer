# Analista de acordes (progresiones musicales)
Un script hecho en Python que permitiría, en su versión final, descargar automáticamente hojas de acordes de varios sitios y analizarlas armónicamente (siguiendo el sistema del Berklee College of Music). También incluye funcionalidades
para detectar progresiones específicas, lo cual sería útil para estudiar y clasificar grandes cantidades de canciones, intentar detectar patrones históricos/estilísticos reflejados en la armonía y otras ideas varias.

El análisis realizado se basa en el enseñado en Berklee por su orientación hacia el jazz y la música popular (puede consultarse en [libros como este](https://blackwells.co.uk/bookshop/search/isbn/9780876391426))

## Uso
El script *Teoría* contiene la lógica fundamental para detectar distintos tipos de acordes y progresiones; es importante contemplar todo el material armónico en simultáneo ya que un mismo acorde puede interpretarse de maneras diferentes
según lo que ocurra musicalmente en un momento futuro de la canción. Además, implementa una función experimental que permite detectar si la canción se encuentra en una tonalidad mayor, a partir de un sistema de puntos que intenta reflejar la
experiencia auditiva subjetiva más habitual dentro de los estándares musicales occidentales (la definición contemporánea de tonalidad requiere la detección auditiva de un punto de reposo en un acorde mayor, lo cual es difícilmente 
sistematizable).

El script *Scrapper* permite analizar automáticamente urls de distintos sitios web que funcionan como repositorio de hojas de acordes, detectando si una progresión buscada se encuentra en la canción. Hasta el momento hay implementaciones
para tres sitios: Ultimate Guitar, LaCuerda y AcordesDCanciones.
