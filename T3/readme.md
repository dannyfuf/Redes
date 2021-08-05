# Red 1

## Parte 1
1. Ejecutar Pox
    ```bash
    python2 mininet/pox/pox.py openflow.spanning_tree --no-flood --hold-down openflow.discovery forwarding.parte1
    ```
2. Ejecutar topologia
    ```bash
    sudo mn --custom p1.py --topo topo1 --controller remote --switch ovsk --mac
    ```
3. Ejecutar un Pingall para verificar la conexion de todos los hosts
    ```bash
    mininet> pingall
    ```
4. Quitar una conexion entre switches
    ```bash
    mininet> link s1 s2 down
    ```
5. Ejecutar Pingall para ver el efecto
    ```bash
    mininet> pingall
    mininet> pingall
    ```
6. Reparar el link.
    ```bash
    mininet> link s1 s2 up
    ```