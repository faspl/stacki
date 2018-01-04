# @copyright@
# Copyright (c) 2006 - 2017 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

import os
import stack.commands
from stack.discovery import Discovery
from stack.exception import CommandError
import time


class Command(stack.commands.enable.command):
	"""
	Start the node discovery daemon.

	<param type='string' name='appliance' optional='1'>
	Name of the appliance used to configure discovered nodes. Defaults to 'backend'.
	</param>

	<param type='string' name='appliance' optional='1'>
	The base name for the discovered nodes. Defaults to the appliance name.
	</param>

	<param type='string' name='rack' optional='1'>
	The rack number to use for discovered nodes. Defaults to the 'discovery.base.rack' attribute.
	</param>

	<param type='string' name='rank' optional='1'>
	The rank number to start from when discovering nodes. Defaults to the next availble rank number for the rack.
	</param>
	
	<param type='string' name='box' optional='1'>
	The box used to configure discovered nodes. Defaults to 'default'.
	</param>

	<param type='string' name='installaction' optional='1'>
	The install action used to configure discovered nodes. Defaults to 'default'.
	</param>

	<example cmd='enable discovery'>
	Discover nodes and install the backend appliance using all defaults.
	</example>

	<related>disable discovery</related>
	<related>report discovery</related>
	"""		

	def run(self, params, args):
		discovery = Discovery()

		(appliance, base_name, rack, rank, box, install_action) = self.fillParams([
			("appliance", None),
			("basename", None),
			("rack", None),
			("rank", None),
			("box", None),
			("installaction", None)
		])

		try:
			# Call start
			discovery.start(
				self,
				appliance_name=appliance,
				base_name=base_name,
				rack=rack,
				rank=rank,
				box=box,
				install_action=install_action
			)
			
			# Wait up to a few seconds for the daemon to start
			for _ in range(8):
				# Are we up yet?
				if discovery.is_running():
					self.beginOutput()
					self.addOutput('', "Discovery daemon has started")
					self.endOutput()

					break

				# Take a quarter second nap
				time.sleep(0.25)
			else:
				self.beginOutput()
				self.addOutput('', "Warning: daemon might have not started")
				self.endOutput()
		
		except ValueError as e:
			raise CommandError(self, str(e)) from None