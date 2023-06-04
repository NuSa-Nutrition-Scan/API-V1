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
            'created_at': self.__current_timestamp()
        }

        doc_ref.set(data)

        return data

    def get_count_nutrition_input_today(self, user_id: str) -> int:
        gmt7 = pytz.timezone('Etc/GMT+7')
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

        result = query.get()

        user_nutrition_photos = []

        for r in result:
            doc = {'nutrition_id': r.id}
            doc.update(r.to_dict())

            user_nutrition_photos.append(doc)

        return user_nutrition_photos

    # GMT +7
    def __current_timestamp(self) -> datetime:
        utc_now = datetime.datetime.now(pytz.utc)
        gmt7 = pytz.timezone('Etc/GMT+7')
        gmt7_now = utc_now.astimezone(gmt7)
        print(gmt7_now)
        return gmt7_now
