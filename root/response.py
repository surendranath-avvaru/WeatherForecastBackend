from rest_framework.response import Response


class CustomResponse(Response):

    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        super(Response, self).__init__(None, status=status)

        response_data = {'message':{ 'success': '', 'errors': {} }}
        if status in [200,201]:
            if data == None:
                data={}
            response_data['message']['success'] = True
            response_data['payload'] = {'results':data}
            data = response_data
        else:
            response_data['payload'] = {}
            response_data['message']['success'] = False
            response_data['message']['errors'] = data
            data = response_data

        return super(CustomResponse, self).__init__(data,status,template_name,headers,exception,content_type)

class GenericResponse(Response):

    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        super(Response, self).__init__(None, status=status)

        response_data = {'message':{ 'success': '', 'errors': {} }}
        if status in [200,201]:
            if data == None:
                data={}
            response_data['message']['success'] = True
            response_data['payload'] = data
            data = response_data
        else:
            response_data['payload'] = {}
            response_data['message']['success'] = False
            response_data['message']['errors'] = data
            data = response_data

        return super(GenericResponse, self).__init__(data,status,template_name,headers,exception,content_type)