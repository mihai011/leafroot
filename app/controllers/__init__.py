from fastapi.responses import JSONResponse


def parse(request):

  args = request.path_params

  return args

def create_response_ok(message):

  data = {}  
  data['message'] = message
  data['status'] = 200
  return JSONResponse(content=data)