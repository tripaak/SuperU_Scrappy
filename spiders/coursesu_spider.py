import scrapy 
from ..items import CoursesuItem
import requests
from scrapy.http import TextResponse


def parse_xhr(xhr_url):
    
        response = requests.get(xhr_url)
        response = TextResponse(body=response.content, url=xhr_url)
        slots = response.css('div.slot-info')
        time_slot = {}
        if len(slots) > 1:
            
            if slots.css('p.title::text')[0].get().split()[0] == 'Drive':

                time_slot['Drive'] = slots.css('p.info::text')[0].get().strip()
                time_slot['Livraison'] = slots.css('p.info::text')[1].get().strip()
                             
            elif  slots.css('p.title::text').get().split()[0] == 'Livraison':  
              
                time_slot['Livraison'] = slots.css('p.info::text')[0].get().strip()
                time_slot['Drive'] = slots.css('p.info::text')[1].get().strip()
                
            return time_slot        
                  
        else:


            if slots.css('p.title::text')[0].get().split()[0] == 'Drive':
                 
                time_slot['Drive'] = slots.css('p.info::text')[0].get().strip()
                time_slot['Livraison'] = None
                   
            else:
                
                time_slot['Livraison'] = slots.css('p.info::text')[0].get().strip()
                time_slot['Drive'] = None

            
            return time_slot



class CourseU(scrapy.Spider):
    
    name = 'coursesu'
    start_urls = [
        'https://www.coursesu.com/drive/home'
    ]
     

    def parse(self, response):
       
        for link in response.css('li.stores-group-item a::attr(href)'):
           yield response.follow(link.get(), callback=self.parse_region)
           break


    def parse_region(self, response):
        
        item = CoursesuItem()
        stores = response.css('li.storelocator-store-item')
        for store in stores :

            item['name'] = store.css('div.storelocator-directions h3.store-title::text').get().strip() ,
            item['address']= store.css('div.storelocator-description p.store-description.address::text').get().strip(),
            item['postalcode'] = store.css('div.storelocator-description p.store-description.postalcode::text').get().strip(),
            item['city'] = store.css('div.storelocator-description p.store-description.city::text').get().strip(),

            store_id = store.css('li.storelocator-store-item::attr(id)').get().strip()

            xhr_url = "https://www.coursesu.com/on/demandware.store/Sites-DigitalU-Site/fr_FR/DeliverySlot-RenderClosestPointSlot?storeId="+store_id+"&isMap=false"

 
            time_slot = parse_xhr(xhr_url) #call for XHR request

            item['Drive'] = time_slot['Drive'] ,
            item['Livraison']= time_slot['Livraison']

            yield item

    
             
                 

