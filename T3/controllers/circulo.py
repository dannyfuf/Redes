# Copyright 2011-2012 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
An L2 learning switch.

It is derived from one written live for an SDN crash course.
It is somwhat similar to NOX's pyswitch in that it installs
exact-match rules for each flow.
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str, str_to_dpid
from pox.lib.util import str_to_bool
import time

log = core.getLogger()

# We don't want to flood immediately when a switch connects.
# Can be overriden on commandline.
_flood_delay = 0

class LearningSwitch (object):
  def __init__ (self, connection, transparent):
    # Switch we'll be adding L2 learning switch capabilities to
    self.connection = connection
    self.transparent = transparent

    # Our table
    self.macToPort = {}

    # We want to hear PacketIn messages, so we listen
    # to the connection
    connection.addListeners(self)

    # We just use this to know when to log a helpful message
    self.hold_down_expired = _flood_delay == 0

    #log.debug("Initializing LearningSwitch, transparent=%s",
    #          str(self.transparent))

  def _handle_PacketIn (self, event):
    """
    Handle packet in messages from the switch to implement above algorithm.
    """

    packet = event.parsed
    #print(packet, "HOLA SOY UN PAKETE SIIIIII")
    def flood (message = None):
      """ Floods the packet """
      msg = of.ofp_packet_out()
      if time.time() - self.connection.connect_time >= _flood_delay:
        # Only flood if we've been connected for a little while...

        if self.hold_down_expired is False:
          # Oh yes it is!
          self.hold_down_expired = True
          log.info("%s: Flood hold-down expired -- flooding",
              dpid_to_str(event.dpid))

        if message is not None: log.debug(message)
        #log.debug("%i: flood %s -> %s", event.dpid,packet.src,packet.dst)
        # OFPP_FLOOD is optional; on some switches you may need to change
        # this to OFPP_ALL.
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      else:
        pass
        #log.info("Holding down flood for %s", dpid_to_str(event.dpid))
      msg.data = event.ofp
      msg.in_port = event.port
      self.connection.send(msg)

    def drop (duration = None):
      """
      Drops this packet and optionally installs a flow to continue
      dropping similar ones for a while
      """
      if duration is not None:
        if not isinstance(duration, tuple):
          duration = (duration,duration)
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = duration[0]
        msg.hard_timeout = duration[1]
        msg.buffer_id = event.ofp.buffer_id
        self.connection.send(msg)
      elif event.ofp.buffer_id is not None:
        msg = of.ofp_packet_out()
        msg.buffer_id = event.ofp.buffer_id
        msg.in_port = event.port
        self.connection.send(msg)

    self.macToPort[packet.src] = event.port # 1

    if packet.dst.is_multicast:
      flood()
    else:
      msg = of.ofp_flow_mod()

      # Verificar que solamente puedan acceder los host con mac conocida.
      known_hosts = ["00:00:00:00:00:0"+i for i in range(9)]
      if str(packet.dst) not in known_hosts or str(packet.src) not in known_hosts:
        drop()
        return
      msg.match = of.ofp_match.from_packet(packet, event.port)
      msg.idle_timeout = 10
      print ("Destino: ",str(packet.dst),"Origen: " ,str(packet.src))
      print ("Vengo desde:" ,event.port)
      msg.hard_timeout = 30

      if str(packet.src) == known_hosts[0]  or str(packet.src) == known_hosts[1]: # hosts del s1
        if str(packet.dst) != "00:00:00:00:00:01" and str(packet.dst) != "00:00:00:00:00:02":
          if event.port == 2 or event.port == 4:
            msg.actions.append(of.ofp_action_output(port = 6))
            print("Voy a salir por:", 6)
          elif event.port == 5:
            if str(packet.dst) == "00:00:00:00:00:04":
              msg.actions.append(of.ofp_action_output(port = 18))
              print("Voy a salir por:", 18)
            elif str(packet.dst) == "00:00:00:00:00:03":
              msg.actions.append(of.ofp_action_output(port = 16))
              print("Voy a salir por:", 16)  
            else:
              msg.actions.append(of.ofp_action_output(port = 14))
              print("Voy a salir por:", 14)    
          elif event.port == 13:
            if str(packet.dst) == "00:00:00:00:00:05":
              msg.actions.append(of.ofp_action_output(port = 10))
              print("Voy a salir por:", 10)
            elif str(packet.dst) == "00:00:00:00:00:06":
              msg.actions.append(of.ofp_action_output(port = 12))
              print("Voy a salir por:", 12)  
            else:
              msg.actions.append(of.ofp_action_output(port = 8))
              print("Voy a salir por:", 8)   
        else:
          if str(packet.dst) == "00:00:00:00:00:01":
            port = 2
          else:
            port = 4
          msg.actions.append(of.ofp_action_output(port = port))
          print("Voy a salir por:", port) 


      elif str(packet.src) == "00:00:00:00:00:03"  or str(packet.src) == "00:00:00:00:00:04":
        if str(packet.dst) != "00:00:00:00:00:03" and str(packet.dst) != "00:00:00:00:00:04":
          if event.port == 18 or event.port == 16:
            msg.actions.append(of.ofp_action_output(port = 14))
            print("Voy a salir por:", 14)
          elif event.port == 13:
            if str(packet.dst) == "00:00:00:00:00:05":
              msg.actions.append(of.ofp_action_output(port = 10))
              print("Voy a salir por:", 10)
            elif str(packet.dst) == "00:00:00:00:00:06":
              msg.actions.append(of.ofp_action_output(port = 12))
              print("Voy a salir por:", 12)  
            else:
              msg.actions.append(of.ofp_action_output(port = 8))
              print("Voy a salir por:", 8)    
          elif event.port == 7:
            if str(packet.dst) == "00:00:00:00:00:01":
              msg.actions.append(of.ofp_action_output(port = 2))
              print("Voy a salir por:", 2)
            elif str(packet.dst) == "00:00:00:00:00:02":
              msg.actions.append(of.ofp_action_output(port = 4))
              print("Voy a salir por:", 4)  
            else:
              msg.actions.append(of.ofp_action_output(port = 6))
              print("Voy a salir por:", 6) 
        else:
          if str(packet.dst) == "00:00:00:00:00:03":
            port = 16
          else:
            port = 18
          msg.actions.append(of.ofp_action_output(port = port))
          print("Voy a salir por:", port) 



      elif str(packet.src) == "00:00:00:00:00:05"  or str(packet.src) == "00:00:00:00:00:06":
        if str(packet.dst) != "00:00:00:00:00:05" and str(packet.dst) != "00:00:00:00:00:06":
          if event.port == 10 or event.port == 12:
            msg.actions.append(of.ofp_action_output(port = 8))
            print("Voy a salir por:", 8)
          elif event.port == 7:
            if str(packet.dst) == "00:00:00:00:00:01":
              msg.actions.append(of.ofp_action_output(port = 2))
              print("Voy a salir por:", 2)
            elif str(packet.dst) == "00:00:00:00:00:02":
              msg.actions.append(of.ofp_action_output(port = 4))
              print("Voy a salir por:", 4)  
            else:
              msg.actions.append(of.ofp_action_output(port = 6))
              print("Voy a salir por:", 6)    
          elif event.port == 5:
            if str(packet.dst) == "00:00:00:00:00:04":
              msg.actions.append(of.ofp_action_output(port = 18))
              print("Voy a salir por:", 18)
            elif str(packet.dst) == "00:00:00:00:00:03":
              msg.actions.append(of.ofp_action_output(port = 16))
              print("Voy a salir por:", 16)  
            else:
              msg.actions.append(of.ofp_action_output(port = 14))
              print("Voy a salir por:", 14) 
        else:
          if str(packet.dst) == "00:00:00:00:00:05":
            port = 10
          else:
            port = 12
          msg.actions.append(of.ofp_action_output(port = port))
          print("Voy a salir por:", port)

      else:
        msg.actions.append(of.ofp_action_output(port = port))
        print("Voy a salir por:", port) 
      msg.data = event.ofp # 6a
      #print(msg)
      self.connection.send(msg)

class l2_learning (object):
  """
  Waits for OpenFlow switches to connect and makes them learning switches.
  """
  def __init__ (self, transparent, ignore = None):
    """
    Initialize

    See LearningSwitch for meaning of 'transparent'
    'ignore' is an optional list/set of DPIDs to ignore
    """
    core.openflow.addListeners(self)
    self.transparent = transparent
    self.ignore = set(ignore) if ignore else ()

  def _handle_ConnectionUp (self, event):
    if event.dpid in self.ignore:
      log.debug("Ignoring connection %s" % (event.connection,))
      return
    log.debug("Connection %s" % (event.connection,))
    LearningSwitch(event.connection, self.transparent)


def launch (transparent=False, hold_down=_flood_delay, ignore = None):
  """
  Starts an L2 learning switch.
  """
  try:
    global _flood_delay
    _flood_delay = int(str(hold_down), 10)
    assert _flood_delay >= 0
  except:
    raise RuntimeError("Expected hold-down to be a number")

  if ignore:
    ignore = ignore.replace(',', ' ').split()
    ignore = set(str_to_dpid(dpid) for dpid in ignore)

  core.registerNew(l2_learning, str_to_bool(transparent), ignore)
