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
    def flood (message = None):
      """ Floods the packet """
      msg = of.ofp_packet_out()
      if time.time() - self.connection.connect_time >= _flood_delay:
        
        if self.hold_down_expired is False:
          self.hold_down_expired = True
          log.info("%s: Flood hold-down expired -- flooding",
              dpid_to_str(event.dpid))

        if message is not None: log.debug(message)
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      else:
        pass
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

    self.macToPort[packet.src] = event.port 

    if packet.dst.is_multicast:
      flood()
    else:
      msg = of.ofp_flow_mod()

      ## Hash con la direccion mac de origen como llave y el valor es otro diccionario 
      ## con la direccion mac de destino como llave y como valor otro diccionario 
      ## con el puerto de entrada como llave y como valor el puerto de salida
      forward = {
        "00:00:00:00:00:01":{
          "00:00:00:00:00:03":{
            11: 34,
            12: 34,
            21: 33,
            24: 32,
            23: 13
          },
          "00:00:00:00:00:04":{
            11: 34,
            12: 34,
            21: 33,
            24: 32,
            23: 14
          },
          "00:00:00:00:00:05":{
            11: 34,
            12: 34,
            21: 33,
            24: 15
          },
          "00:00:00:00:00:06":{
            11: 34,
            12: 34,
            21: 33,
            24: 16
          },
          "00:00:00:00:00:07":{
            11: 34,
            12: 34,
            21: 17
          },
          "00:00:00:00:00:08":{
            11: 34,
            12: 34,
            21: 18
          }
        },
        "00:00:00:00:00:02":{
          "00:00:00:00:00:03":{
            11: 34,
            12: 34,
            21: 33,
            24: 32,
            23: 13
          },
          "00:00:00:00:00:04":{
            11: 34,
            12: 34,
            21: 33,
            24: 32,
            23: 14
          },
          "00:00:00:00:00:05":{
            11: 34,
            12: 34,
            21: 33,
            24: 15
          },
          "00:00:00:00:00:06":{
            11: 34,
            12: 34,
            21: 33,
            24: 16
          },
          "00:00:00:00:00:07":{
            11: 34,
            12: 34,
            21: 17
          },
          "00:00:00:00:00:08":{
            11: 34,
            12: 34,
            21: 18
          }
        },
        "00:00:00:00:00:03":{
          "00:00:00:00:00:01":{
            13: 31,
            22: 11
          },
          "00:00:00:00:00:02":{
            13: 31,
            22: 12
          },
          "00:00:00:00:00:05":{
            13: 31,
            22: 34,
            21: 33,
            24: 15
          },
          "00:00:00:00:00:06":{
            13: 31,
            22: 34,
            21: 33,
            24: 16
          },
          "00:00:00:00:00:07":{
            13: 31,
            22: 34,
            21: 17
          },
          "00:00:00:00:00:08":{
            11: 34,
            12: 34,
            21: 18
          }
        },
        "00:00:00:00:00:04":{
          "00:00:00:00:00:01":{
            14: 31,
            22: 11
          },
          "00:00:00:00:00:02":{
            14: 31,
            22: 12
          },
          "00:00:00:00:00:05":{
            14: 31,
            22: 34,
            21: 33,
            24: 15
          },
          "00:00:00:00:00:06":{
            14: 31,
            22: 34,
            21: 33,
            24: 16
          },
          "00:00:00:00:00:07":{
            14: 31,
            22: 34,
            21: 17
          },
          "00:00:00:00:00:08":{
            14: 34,
            12: 34,
            21: 18
          }
        },
        "00:00:00:00:00:05":{
          "00:00:00:00:00:01":{
            15: 32,
            23: 31,
            22: 11
          },
          "00:00:00:00:00:02":{
            15: 32,
            23: 31,
            22: 12
          },
          "00:00:00:00:00:03":{
            15: 32,
            23: 13
          },
          "00:00:00:00:00:04":{
            15: 32,
            23: 14
          },
          "00:00:00:00:00:07":{
            15: 32,
            23: 31,
            22: 34,
            21: 17
          },
          "00:00:00:00:00:08":{
            15: 32,
            23: 31,
            22: 34,
            21: 18
          }
        },
        "00:00:00:00:00:06":{
          "00:00:00:00:00:01":{
            16: 32,
            23: 31,
            22: 11
          },
          "00:00:00:00:00:02":{
            16: 32,
            23: 31,
            22: 12
          },
          "00:00:00:00:00:03":{
            16: 32,
            23: 13
          },
          "00:00:00:00:00:04":{
            16: 32,
            23: 14
          },
          "00:00:00:00:00:07":{
            16: 32,
            23: 31,
            22: 34,
            21: 17
          },
          "00:00:00:00:00:08":{
            16: 32,
            23: 31,
            22: 34,
            21: 18
          }
        },
        "00:00:00:00:00:07":{
          "00:00:00:00:00:01":{
            17: 33,
            24: 32,
            23: 31,
            22: 11
          },
          "00:00:00:00:00:02":{
            17: 33,
            24: 32,
            23: 31,
            22: 12
          },
          "00:00:00:00:00:03":{
            17: 33,
            24: 32,
            23: 13
          },
          "00:00:00:00:00:04":{
            17: 33,
            24: 32,
            23: 14
          },
          "00:00:00:00:00:05":{
            17: 33,
            24: 15
          },
          "00:00:00:00:00:06":{
            17: 33,
            24: 16
          }
        },
        "00:00:00:00:00:08":{
          "00:00:00:00:00:01":{
            18: 33,
            24: 32,
            23: 31,
            22: 11
          },
          "00:00:00:00:00:02":{
            18: 33,
            24: 32,
            23: 31,
            22: 12
          },
          "00:00:00:00:00:03":{
            18: 33,
            24: 32,
            23: 13,
          },
          "00:00:00:00:00:04":{
            18: 33,
            24: 32,
            23: 14,
          },
          "00:00:00:00:00:05":{
            18: 33,
            24: 15
          },
          "00:00:00:00:00:06":{
            18: 33,
            24: 16
          }
        }
      }

      # Definir lista con todas las mac de host connocidos  
      known_hosts = ["00:00:00:00:00:0"+i for i in range(1, 9)]
      msg.match = of.ofp_match.from_packet(packet, event.port)
      msg.idle_timeout = 10
      mac_dst = str(packet.dst)
      mac_src = str(packet.src)
      port = event.port
      print ("Mac dst: ",mac_dst,"\nMac src: " ,mac_src)
      print ("port:" , port)
      msg.hard_timeout = 30
      if packet.find('tcp'):
        if mac_src == mac_dst:
          port_out = known_hosts[int(mac_src[-1])-1]
          msg.actions.append(of.ofp_action_output(port = port_out))
        elif mac_src in known_hosts: # hosts del s1
          port_out = forward[mac_src][mac_dst][port]
          msg.actions.append(of.ofp_action_output(port = port_out))
        else:
          print ("No se reconoce el host")
          drop(1)

        msg.data = event.ofp # 6a
        self.connection.send(msg)
      else:
        print("No se aceptan conecciones HTTP")
        drop(1)

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

