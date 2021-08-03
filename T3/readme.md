1. Ejecutar Pox
```bash
python2 mininet/pox/pox.py openflow.spanning_tree --no-flood --hold-down openflow.discovery forwarding.l2_learning
```
2. ejecutar topologia
```bash
sudo mn --custom p1.py --topo topo1 --controller remote --switch ovsk --mac
```