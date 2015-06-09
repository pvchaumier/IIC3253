# TAREA 2 : Chat decentralizado y seguro

## Descipcion

La idea es de hacer un chat que sea decentralizado y seguro. Para hacer eso, utilizo

## Hipotesis

Para hacer esta tarea, hice algunas suposiciones.

- la llaves estan compartidas sin problemas de man in the middle attack
- que no es importante saber de donde a donde van los messajes

## Que falta

- la possibilidad de crear grupos de discusion
- signature : tuve muchos problemas con las signatures. Como utilizo pycrypto, no puedo encryptar messajes que son mas grande que las llaves. Asi un messaje con si signature era demasiado grande y no pude encryptar y decryptarlo.
