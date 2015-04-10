#!/usr/bin/python

#
# UCS Health Check
#
# Rusty Buzhardt and Tighe Kuykendall
#
#
#

from pprint import pprint
from UcsSdk import *
from UcsSdk.MoMeta.NetworkElement import NetworkElement
from UcsSdk.MoMeta.EquipmentManufacturingDef import EquipmentManufacturingDef
from UcsSdk.MoMeta.EquipmentChassis import EquipmentChassis 
from UcsSdk.MoMeta.ComputeBlade import ComputeBlade
from UcsSdk.MoMeta.EquipmentIOCard import EquipmentIOCard
from UcsSdk.MoMeta.FirmwareBootUnit import FirmwareBootUnit
from UcsSdk.MoMeta.FaultInst import FaultInst
import string
import json
import getpass

if __name__ == "__main__":

	try:
#		
# Prompt for UCS Domain login information.
#				
		print ""
		print ""
		print "Welcome To The UCS Health Check Script"
		print ""
		print "Let's get started by collecting some information."
		print "Please enter information about the UCS Domain, a Read-Only login is required."
		print ""
		IP = raw_input("FI IP address: ")
        	username = raw_input("Username: ")
         	password = getpass.getpass("Password: ")
#
# Create the connection to the UCS Domain.
#
		handle = UcsHandle()
		handle.Login(IP, username, password)
                handle.StartTransaction()

#
# Show information about the Fabric Interconnects.
#

		print "FI's"
		print "Serial,DN,Model,OOB,Running Firmware"
		for fi in handle.GetManagedObject(None, NetworkElement.ClassId()):
			model = handle.GetManagedObject(None, EquipmentManufacturingDef.ClassId(), {"Pid":fi.Model})
                        code = handle.GetManagedObject(None, FirmwareBootUnit.ClassId())
			print fi.Serial + "," + fi.Dn + "," + model[0].Name.replace("Cisco UCS ", "") + "," + fi.OobIfIp + "," + code[0].Version

#
# Show information about the Chassis.
#

		print "\nChassis"
		print "Serial,DN,Model"
		for chassis in handle.GetManagedObject(None, EquipmentChassis.ClassId()):
			model = handle.GetManagedObject(None, EquipmentManufacturingDef.ClassId(), {"Pid":chassis.Model})
			print chassis.Serial + "," + chassis.Dn + "," + model[0].Name.replace("Cisco UCS ", "")

#
# Show information about the IOM's.
#

		print "\nIOM's"
		print "Chassis Number,Fabric ID,Model,Serial,Running Firmware,Backup Firmware"
		for iom in handle.GetManagedObject(None, EquipmentIOCard.ClassId()):
			model = handle.GetManagedObject(None, EquipmentManufacturingDef.ClassId(), {"Pid":iom.Model})
			runningVersion = handle.GetManagedObject(None, FirmwareBootUnit.ClassId())
			print iom.ChassisId + "," + iom.SwitchId + " ("+ iom.Side + ")" + "," + model[0].Name.replace("Cisco UCS ", "") + "," + iom.Serial + "," + runningVersion[0].Version + "," + runningVersion[0].PrevVersion

#
# Show information about the Blades.
#

		print "\nBlades"
		print "Serial,DN,Model,Assigned,Total Memory,Running Fimware,Backup Firmware"
		for blade in handle.GetManagedObject(None, ComputeBlade.ClassId()):
			model = handle.GetManagedObject(None, EquipmentManufacturingDef.ClassId(), {"Pid":blade.Model})
			runningVersion = handle.GetManagedObject(None, FirmwareBootUnit.ClassId())
			print blade.Serial + "," + blade.Dn + "," + model[0].Name.replace("Cisco UCS ", "") + "," + blade.AssignedToDn + "," + blade.TotalMemory + "," + runningVersion[0].Version + "," + runningVersion[0].PrevVersion

                print "\nFaults in system"
                print "Severity, DN, Description"
                for fault in handle.GetManagedObject(None, FaultInst.ClassId()):
                        print fault.Severity + "," + fault.Dn + "," + fault.Descr
	
                handle.CompleteTransaction()
		handle.Logout()


	except Exception, err:
		print "Exception:", str(err)
		import traceback, sys
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60
		handle.Logout()
