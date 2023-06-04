import datetime
import pytz
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud import firestore

class Firestore:
    def __init__(self, db):
        self.db = db

    def save_nutrition_data(self, user_id: str, img_url: str) -> dict:
        doc_ref = self.db.collection('user_nutrition').document()

        data = {
            'user_id': user_id,
            'img_url': img_url,
            'created_at': self.__curr_time().strftime("%Y-%m-%d %H:%M:%S")
        }

        doc_ref.set({
            'user_id': user_id,
            'img_url': img_url,
            'created_at': self.__curr_time()
        })

        return data

    def get_count_nutrition_input_today(self, user_id: str) -> int:
        gmt7 = pytz.timezone('Asia/Jakarta')
        now_gmt7 = datetime.datetime.now(gmt7)
        start_of_day_gmt7 = datetime.datetime(
            now_gmt7.year, now_gmt7.month, now_gmt7.day, tzinfo=gmt7)
        end_of_day_gmt7 = start_of_day_gmt7 + datetime.timedelta(days=1)

        collection_ref = self.db.collection('user_nutrition')
        query = collection_ref.where(
            filter=FieldFilter(field_path='user_id',
                               op_string='==', value=user_id)
        ).where(
            filter=FieldFilter(field_path='created_at',
                               op_string='>=', value=start_of_day_gmt7)
        ).where(
            filter=FieldFilter(field_path='created_at',
                               op_string='<', value=end_of_day_gmt7)
        ).count()

        result = query.get()

        return result[0][0].value

    def get_all_user_nutrition_photo(self, user_id: str, skip: int) -> list:
        collection_ref = self.db.collection('user_nutrition')
        page_size = 10

        query = collection_ref.where(
            filter=FieldFilter(field_path='user_id',
                               op_string='==', value=user_id)
        ).order_by(
            'created_at', direction=firestore.Query.DESCENDING
        ).limit(page_size)

        if skip > 0:
            query = query.start_after({ 'created_at': skip * page_size })

        results = query.get()

        user_nutrition_photos = []

        for result in results:
            r = result.to_dict()

            print(r['created_at'])
            doc = {
                'nutrition_id': result.id,
                'img_url': r['img_url'],
                'user_id': r['user_id'],
                'created_at': self.__convert_utc_to_utc7(r['created_at']),
            }

            user_nutrition_photos.append(doc)

        return user_nutrition_photos

    # GMT +7
    def __curr_time(self) -> datetime:
        tz_jakarta = pytz.timezone('Asia/Jakarta')
        datetime_jakarta = datetime.datetime.now(tz_jakarta)
        return datetime_jakarta
    
    def __convert_utc_to_utc7(self, utc_timestamp) -> str:
        utc7_tz = pytz.timezone('Asia/Jakarta')
        utc7_timestamp = utc_timestamp.astimezone(utc7_tz)

        utc7_timestamp_str = utc7_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return utc7_timestamp_str