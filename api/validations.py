from django.http import JsonResponse
from functools import wraps

def validate_query_params(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        # validate text
        warnings = []
        param = request.query_params.get('q', None)
        if param is not None and not isinstance(param, str):            
            warnings.append('El parametro q debe ser de tipo String')                     
        # Aquí puedes agregar más validaciones según tus necesidades
        param = request.query_params.get('c', None)
        if param is not None and param not in ['name', 'country', 'score']:
            warnings.append('El atributo c no es valido')                     
        param2 = request.query_params.get('o', None)
        if param2 is not None  and param2 not in ['asc', 'desc']:
            warnings.append('El atributo o debe ser de tipo asc o desc')                     
        if param is None and param2 is not None:
             warnings.append('Se requiere un atributo para ordenar.')                     
        if len(warnings) > 0 :
            return JsonResponse({'errors': warnings}, status=400)
        
        return func(self, request, *args, **kwargs)
    return wrapper