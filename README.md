# ScalableRecommendSystem
A distributed, scalable and fail tollerance Recommend System using large data.

# RUN 

1. Clone repository 
```bash
  git clone https://github.com/luismoroco/ScalableRecommendSystem.git
```
2. Init data and virtual enviorement VENV: (s) SMALL data 1MB || (f) FULL data 256MB
For example in SMALL data:
```bash
  bash ./setup.sh f 
```

3. Activate your VENV in your directory
```bash
  source venv/bin/activate
```

4. Setup the Cluster - DEV mode: (1)web + (2)Spark[master, node] + (1)db cassandra with REPLICATION=1
```bash
  sudo make setup
```

5. Start the preprocess. This contain a- clean data b-store data in db
```bash
  sudo make preprocess
```

6. For stop the container
```bash
  sudo make down
```
# SPARK 

1. For use SPARK-MASTER. The files for be executed are in /app
```bash
  sudo docker exec -it spark-master bash
  cd app
```


# Architecture

<image
  src="docs/img/Architecture.png"
  alt="Arquitectura propuesta para el sistema de recomendación"
  caption="Arquitectura propuesta para el sistema de recomendación">

* Los datos de MovieLens se importan y almacenan en la base de datos Cassandra, aprovechando su capacidad de escalabilidad y alta disponibilidad
* Spark se utiliza para procesar los datos almacenados en Cassandra y realizar tareas de análisis, como la construcción de modelos de recomendación. Esto implica la ejecución de algoritmos de filtrado colaborativo o enfoques basados en contenido para generar recomendaciones personalizadas
* Una vez generadas las recomendaciones, Flask se encarga de proporcionar una interfaz de usuario y API para que los usuarios puedan interactuar con el sistema. Los usuar- ios pueden realizar consultas de recomendación, recibir resultados y ver información detallada sobre las películas recomendadas.
* El sistema de recomendación basado en Flask, Spark y Cassandra se puede empaquetar en contenedores Docker para facilitar su despliegue y gestión en diferentes entornos.

# Base de datos Cassandra
La base de datos de películas contiene las siguientes tablas:


<image
  src="docs/img/data_base.png">




# Resultados

Cantidad de peliculas que han recibido intervalos de 0-50, 50-100, 100-200 y 200+ count_rating 
<image
  src="docs/img/count_rat_per_intervals.png"
  alt="Distribución de Count Rating en películas">



  rating count representa el número de ratings o calificaciones que recibió la película i, i <= n donde n es el número de películas. La densidad de ratings se encuentra entre < 0 : 3000 <, con valores atípicos

  

  <image
  src="docs/img/rating_count.png"
  alt="Arquitectura propuesta para el sistema de recomendación"
  caption="Arquitectura propuesta para el sistema de recomendación">

  La relación de raing_avg y rating_count, es de- cir el promedio de calificaciones de una película con el número de calificaciones. Se infiere que en muchos casos, el promedio de calificaciones de una película es proporcional al número de interacciones que reciben.

<image
  src="docs/img/rat_avg_rating_count.png"
  alt="Arquitectura propuesta para el sistema de recomendación"
  caption="Arquitectura propuesta para el sistema de recomendación">



  

Este gráfico corresponde a los usuarios: count_rat indica el número de ratings dado por cada usuario y avg_rat. Se infiere una distribución, parecida a la gaussiana.


  <image
  src="docs/img/usr_count_rat_avg_rat.png"
  alt="Arquitectura propuesta para el sistema de recomendación"
  caption="Arquitectura propuesta para el sistema de recomendación">
  
Aquí se explora el dataset tags.csv, las etiquetas asociadas a las películas. Aquí, se muestran algunos valores muy atípicos que tendrán un impacto negativo en el sistema. Podrían considerarse outliers. El mayor grupo de tags se encontraban entre < 0; 200 <.

  <image
  src="docs/img/tags_by_movie.png"
  alt="Arquitectura propuesta para el sistema de recomendación"
  caption="Arquitectura propuesta para el sistema de recomendación">



  Aquí se representa la relación entre rating_avg (promedio de calificaciones por película) y count_tags (número de tags por película). Podemos inferir que en un gran número de casos, mientras más tags tenga una película, mayor es el promedio de calificación. Esto puede deberse a que las películas con más tags son más populares y, por lo tanto, tienen más calificaciones.

<image
  src="docs/img/mov_rating_avg_count_tags.png"
  alt="Arquitectura propuesta para el sistema de recomendación"
  caption="Arquitectura propuesta para el sistema de recomendación">

El mejor tiempo de ejecución agregando más nodos al
cluster

  <image
  src="docs/img/spar_time_cluster.png"
  alt="Arquitectura propuesta para el sistema de recomendación"
  caption="Arquitectura propuesta para el sistema de recomendación">