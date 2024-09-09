import os
import requests
import json
from requests_toolbelt import MultipartEncoder

class LarkSuiteCredentialsFetcherupload:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        url = 'https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'app_id': self.app_id,
            'app_secret': self.app_secret
        }
        print("Waiting for response from lark base")
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        print("Response Recieved")
        return response.json()['tenant_access_token']
    
    def upload_pdf(self, pdf_path):
        url = "https://open.larksuite.com/open-apis/drive/v1/medias/upload_all"
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        pdf_path = f"invoices/{pdf_path}"
        file_size = os.path.getsize(pdf_path)
        extra_param = json.dumps({"bitablePerm": {"tableId": 'tbldOHKaqXLDEw4W'}})
        form = {'file_name': pdf_path,
            'parent_type': 'explorer',
            'size': str(file_size),
            'parent_type': 'bitable_file',
            "parent_node": "AmtqbJV4raGoSYs7xInuIxP8sXg",
            'extra': extra_param,
            'file': (open(pdf_path, 'rb'))}
        multi_form = MultipartEncoder(form)
        headers['Content-Type'] = multi_form.content_type

        response = requests.post(url, headers=headers, data=multi_form)
        data = response.json()
        return data['data']['file_token']

    def update_specific_cell(self, table_id, record_id, field_id, file_key, inv_ref_id):
        url = f'https://open.larksuite.com/open-apis/bitable/v1/apps/AmtqbJV4raGoSYs7xInuIxP8sXg/tables/tbldOHKaqXLDEw4W/records/batch_update'
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        inv_ref_id = str(inv_ref_id)
        data = {
            "records":[
                {
                    "record_id": record_id,
                    "fields": {
                        "Send detail to clients": True,
                        'Invoice Reference ID':inv_ref_id,
                        "Invoice":[
                            {"file_token": file_key}
                        ]
                    }
                }
            ]

        }

        print("Updating specific cell in Lark base table")
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        print("Cell updated")
        return response.json()
    

    def upload_invoic_to_base(record_id, inv_ref_id, pdf_path):

        app_id = 'cli_a4c43163ceb85009'
        app_secret = 'v568vapQUJSC06DokmmvkfD7uBL8AyDW'
        table_id = 'tbldOHKaqXLDEw4W'
        record_id = record_id  # Replace with your record id

        inv_ref_id = inv_ref_id
        pdf_path = pdf_path

        lark_suite = LarkSuiteCredentialsFetcherupload(app_id, app_secret)


        file_key = lark_suite.upload_pdf(pdf_path)

        response = lark_suite.update_specific_cell(
            table_id=table_id,
            record_id=record_id,
            field_id = "Invoice",
            file_key=file_key,
            inv_ref_id = inv_ref_id  
        )

        print(response)