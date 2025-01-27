
```
+-----------------------+       +------------------------+       +-----------------------------+
|        User           |       |         Plot           |       |    CaracteristicasParcela   |
|-----------------------|       |------------------------|       |-----------------------------|
| - id (Primary Key)    |<-M2M->| - id (Primary Key)     |<-1to1-| - id (Primary Key)          |
| - username            |       | - name                 |       | - plot (OneToOne with Plot) |
| - email               |       | - bounds (PolygonField)|       | - identificacion            |
| ...                   |       |                        |       | - parcela_catastral         |
+-----------------------+       |                        |       | - sup_total                 |
                                 |                        |       | - sup_regable               |
                                 |                        |       | - num_olivos                |
                                 +------------------------+       | - concesion                |
                                                                  | - toma_agua                |
                                                                  | - suelo                    |
                                                                  | - paraje                   |
                                                                  | - fecha_alta               |
                                                                  +-----------------------------+
                                                                            |
                                                                            |
                           +------------------------+                       |
                           |       UsoParcela       |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - parcela (ForeignKey) |-----------------------+
                           | - cultivo (ForeignKey) |
                           | - superficie           |
                           | - sistema_riego        |
                           | - estado               |
                           | - fecha_alta           |
                           | - fecha_baja           |
                           +------------------------+
                                                                            |
                           +------------------------+                       |
                           |  ContadoresMedidas     |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - parcela (ForeignKey) |-----------------------+
                           | - contador             |
                           | - fecha_alta           |
                           | - fecha_baja           |
                           | - lectura_max          |
                           +------------------------+
                                                                            |
                           +------------------------+                       |
                           |       Consumos         |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - parcela (ForeignKey) |-----------------------+
                           | - numero_factura       |
                           | - periodo_facturacion  |
                           | - volumen_medido       |
                           | - comentario           |
                           +------------------------+
                                                                            |
                           +------------------------+                       |
                           |   DatosAdicionales     |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - parcela (ForeignKey) |-----------------------+
                           | - tipo_dato            |
                           | - valor                |
                           +------------------------+
                                                                            |
                           +------------------------+                       |
                           |     ControlPagos       |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - parcela (ForeignKey) |-----------------------+
                           | - factura              |
                           | - numero_factura       |
                           | - pagador              |
                           | - vencimiento          |
                           | - total                |
                           +------------------------+
                                                                            |
                           +------------------------+                       |
                           |       Cultivo          |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - nombre               |
                           +------------------------+
                                                                            |
                           +------------------------+                       |
                           |     FaseCultivo        |                       |
                           |------------------------|                       |
                           | - id (Primary Key)     |                       |
                           | - cultivo (ForeignKey) |-----------------------+
                           | - fase                 |
                           | - kc                   |
                           | - nap                  |
                           | - prof_rad             |
                           | - das_inicio           |
                           | - porcentaje_almacen   |
                           +------------------------+
```