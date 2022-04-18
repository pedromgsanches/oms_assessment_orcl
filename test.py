import re

def compareValues(GotValue, ExpecValue, inputOp):
  outputValue=False

  if inputOp == 'equal':
      if GotValue == ExpecValue:
        outputValue = True
  if inputOp == 'greater':
      if GotValue > ExpecValue:
        outputValue = True
  if inputOp == 'less':
      if GotValue < ExpecValue:
        outputValue = True
  if inputOp == 'or':
      match = re.findall(re.escape(GotValue), ExpecValue)
      if match:
        outputValue = True
  return(outputValue)


print(compareValues("quick bananas","the\|quick bananas|brown|fox",'or'))
