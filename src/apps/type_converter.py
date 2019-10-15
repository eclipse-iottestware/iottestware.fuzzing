# ********************************************************************************
# Copyright (c) 2019 Alexander Kaiser
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0.
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors:
#   Alexander Kaiser - initial API and implementation
# ********************************************************************************
import src.utils.type_conversion as tc

# some examples to demonstrate the two different types
example_octstring = "'DEADBEEF'O"
example_bytestring = "b'\\xde\\xad\\xbe\\xef'"


def convert(args):
    input_value = args.input

    output_value = ''   # empty init of output_value
    if args.o:
        output_value = tc.octstring2bytestring(input_value)
    elif args.b:
        input_value = args.input
        output_value = tc.bytestring2octstring(input_value)

    print('{}'.format(output_value))
