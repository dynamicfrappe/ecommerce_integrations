import json 
import base64
import requests

import frappe 




def get_item_shopify_item_code (item_code) :
    """
    params :
            item_code : string erpnext item code 
            return string shopify product code 
            
    """
    return  frappe.get_doc("Ecommerce Item" , {"erpnext_item_code" :item_code} ,
                         "integration_item_code") or False



def get_item_images(item_code) :

    """
    params :
        item_code : string erpnext item code 
    return  [{"image_name" :"Name", "image_path" : "image file full Path"}]        
        
    """

    data = []
    images = frappe.get_list("File" ,filters={"attached_to_doctype" :"Item" ,
                    "attached_to_name" :item_code} ,fields=['file_url' , 'is_private' , 'file_name'])
    n = 1
    if len(images) > 0 :
        for image in images :
            is_private = 'private' if image.get("is_private") else 'public' 
            image_path = frappe.get_site_path(is_private, 'files', image.get("file_name"))
            with open(image_path, mode='rb') as file:
                img = file.read()
            obj = {"image": 
                    {
                    "position":n,
                    "filename" : image.get("file_name") , 
                    "attachment": base64.encodebytes(img).decode()} }

            data.append(obj)
            n+=1

    return data 


@frappe.whitelist()
def send_images_to_shopify(item_code) :
    item_shopify_code = get_item_shopify_item_code(item_code)
    if item_shopify_code :
        url = f"https://elliehome.myshopify.com/admin/api/2024-01/products/{item_shopify_code}/images.json"
        header = {"X-Shopify-Access-Token": "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" ,
        "Content-Type": "application/json"}

        images_data = get_item_images(item_code)
        if images_data : 
            for payload in images_data :
                r = requests.post(url , data = json.dumps(payload) , headers=header)
                frappe.msgprint(r.text)
        else :
            frappe.msgprint("No Images Found")
    else :
        frappe.throw("Error Accourd ")
