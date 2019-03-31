from django.core.management.base import BaseCommand, CommandError
from ...models import DetalleWeb 
import io
import pandas as pd
import requests
import xlrd
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from ...loger import Loger as log
import pytz

class Command(BaseCommand):
    
    help = 'help'

    ###################################3
    # add arguments to this class 
    # and parse it
    
    def add_arguments(self, parser):
     try:  
        parser.add_argument('-s', '--start', type=str, help='Define a start-time eg. --start yyy-mm--dd or -s yyy-mm-dd' , )
        parser.add_argument('-e', '--end', type=str, help='Define a end-time eg. --end yyy-mm-dd or -e yyy-mm--dd', )
        parser.add_argument('-m', '--month',  type=str, help='Get three months from today to three month ago', )
     except AttributeError as e:
            self.stderr.write(str(e))
   
    def handle(self, *args, **options):
     try:
         if options['start']: 
           self.stderr.write("getting a range of days")
           detallesweb = CableMovilAPI()
           detallesweb.get_records( options['start'], options['end'])
         elif options['month']:
           detallesweb = CableMovilAPI()
           detallesweb.get_three_month()
           self.stderr.write("getting three month s")
     except AttributeError as e:
        self.stderr.write(str(e))

   
 ###################################
 # we create a clas to handle the call to the api from cablemovil an we get all the data from it 
 # this class were defined by Javier Matos at vozplus
    
class CableMovilAPI(object):


    log = log('log.txt','consumos_web')
    USERNAME = '216325'
    PASSWORD = 'yDR0nc3QQy'
    code = ''
    consumos = []
    detalles_web = []
    def __init__(self):
        self.log.log_info('Logeandose')
        self.session = requests.Session()
        self.session.get('http://operadores.cablemovil.es/')
        self.session.post(
            'http://operadores.cablemovil.es/index.php',
            params={
                'access': 'CableAccess',
            },
            data={
                'usertype': 'C',
                'username': self.USERNAME,
                'password': self.PASSWORD,
                
            }
        )


    def get_consume(self,start, end):
        # http://operadores.cablemovil.es/index.php?action=cableOperadores::clientes::clientes::ListProductosMovil
     
        response = self.session.post(
            url='http://operadores.cablemovil.es/index.php?action=cableOperadores::cdrs::GetCdrs',
            data={
                'excel': 1,
                'envio': 'Consultar',
                'fechaIni': start,
                'fechaFin': start,
                'id_cliente':'216325',
                'ani':'',
                'tipoCdrs':'ambos'

            },
        )
        data = io.BytesIO(response.content).read()
        self.code = response.status_code
        book = xlrd.open_workbook(file_contents=data, encoding_override='cp1252')
        x1 = pd.ExcelFile(book, engine='xlrd')
        # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_excel.html
        df = x1.parse(
            na_values=None,
            keep_default_na=False,
            converters={i: str for i in range(book.sheet_by_index(0).ncols)},
        )
      
        return [{k: v for k, v in row_data.iteritems()} for row_number, row_data in df.iterrows()]
 
 
    def flip_date(self, date, time):
        
         date = date.split('-')
         time = time.split(':')
     
         date = datetime(year=int(date[2]), month=int(date[1]), day=int(date[0]), hour=int(time[0]), minute=int(time[1]), second=int(time[2]))    
         return date.strftime("%Y-%m-%d %H:%M:%S")
    def flip_month(self, date, time):
         date = date.split('-')
         time = time.split(':')
     
         date = datetime(year=int(date[2]), month=int(date[1]), day=int(date[0]), hour=int(time[0]), minute=int(time[1]), second=int(time[2]), tzinfo=pytz.UTC)    
         return date
 
 ###################################
 # we create a report and we record it in to de db
     
    def crear_report(self,consumo_web,date):
        print('registering one', consumo_web)
      
        i = 0
        details = []
             
        for x in  :
               try:      
                    for c in x:
                                     
                           defaults = {'origen': c['Origen'], 'destino': c['Destino'], 'detalle_destino': c['Detalle Destino'], 'fecha': self.flip_date(c['Fecha'],c['Hora']), 'hora': self.flip_date(c['Fecha'],c['Hora']), 'duracion': c['DuraciÃ³n'], 'datos_MB':c['Datos (MB)'], 'precio': c['Precio'], 'tarifa': c['Tarifa'], 'mes': self.flip_month(c['Fecha'],c['Hora']).month, 'ano': self.flip_month(c['Fecha'],c['Hora']).year }
                           try:
                               obj = DetalleWeb.objects.get( origen=c['Origen'], destino=c['Destino'], fecha=self.flip_date(c['Fecha'],c['Hora']), hora=self.flip_date(c['Fecha'],c['Hora']) )
                               
                           except DetalleWeb.DoesNotExist:
                            
                               obj = DetalleWeb(**defaults)
                             
                               details.append(obj)
                           except DetalleWeb.MultipleObjectsReturned:
                               print('Duplicate : {}'.format(c))
               except IndexError as e:
                       print(e,c)
        print('Saving objects into the db')               
        DetalleWeb.objects.bulk_create(details)             
             
                 
             
 ###################################
 # we get a range of date from the web api
 #              
    def get_range(self,start,end):
         flag = True
         i = 0
         print(start,end)
         start= start.split('-')
         end = end.split('-')
         start = datetime(int(start[0]), int(start[1]), int(start[2]))
         end = datetime(int(end[0]), int(end[1]), int(end[2]))
         days = (end-start)
         print(days)
         if str(days) != '0:00:00':
              days = str(days).split(' ')
              days = days[0]
         else:
              days = 1     
        
        
         while flag:  
          
              try:  
                  for x in range((int(days))):
                       i += 1
                       nexto = str(start.date()).split('-')
                       start_range = str(nexto[2]+'-'+nexto[1]+'-'+nexto[0])
                       self.consumos.append( self.get_consume(start_range,start_range) )
                       start +=  timedelta(days=1)
                       print('days',days,i)
                  if i >= int(days):
                        flag = False  
              except xlrd.biffh.XLRDError as e:
                   
                   print('Mes no existe',e,'days: ',i )
                   start +=  timedelta(days=1)  
                   if i >= int(days):
                       flag = False
         print('FInish the call to the api')              
         self.crear_report(self.consumos,start.date())
     
       
         return self.consumos


 ###################################
 # method who start  recording    

    def get_records(self,start, end):

        self.get_range(start,end)

###################################
 # method to record three months completely  

    def get_three_month(self):

        today = datetime.now()
        month = today - timedelta(days=90)
        print(month.strftime('%Y-%m-%d'))
        self.get_range(month.strftime('%Y-%m-%d'),today.strftime('%Y-%m-%d'))
        print('get')
           
   
        