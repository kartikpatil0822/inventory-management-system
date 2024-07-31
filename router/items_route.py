import json
import logging

from fastapi import APIRouter, Depends, Request, responses, status, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db, get_redis_pool
from logging_config import setup_logging

router = APIRouter()
setup_logging()


@router.post('/items/')
async def create_item(request: Request, db: Session = Depends(get_db)):
    logging.info(f"Request method: ['{request.method}'], url: {request.url}, headers: {request.headers}, "
                 f"body: {request.body}")
    try:
        data = await request.json()
        item_name = data.get('itemname')
        item_desc = data.get('itemdesc')

        logging.info(f'Creating item with name: {item_name} and desc: {item_desc}')
        query = 'INSERT into items (itemname, itemdesc) VALUES (:item_name, :item_desc)'

        logging.info(f'Executing query: {query} to create item')
        db.execute(text(query), {'item_name': item_name, 'item_desc': item_desc})
        db.commit()

        logging.info(f'Executing query: {query} to get itemid')
        query = 'SELECT itemid from items WHERE itemname = :item_name'
        itemid = db.execute(text(query), {'item_name': item_name, 'item_desc': item_desc}).fetchone()
        itemid = itemid.itemid
        print(itemid)
        response = responses.JSONResponse(status_code=status.HTTP_201_CREATED,
                                          content={'item_name': item_name, 'item_desc': item_desc})

        logging.info(f"Request: method: ['{request.method}'], url: {request.url}, headers: {request.headers}, "
                     f"body: {request.body}:: Response: status_code = {response.status_code}, content = {response.body}")
        return response

    except Exception as e:
        response = responses.JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                          content={'error': 'Item already exists.'})
        logging.error(f"Request: method: ['{request.method}'], url: {request.url}, headers: {request.headers}, "
                      f"body: {request.body}:: Response: status_code = {response.status_code}, content = {response.body}")
        return response


@router.get('/items/{item_id}')
async def get_item(item_id: str, request: Request, db: Session = Depends(get_db),
                   redis_instance: any = Depends(get_redis_pool)):
    logging.info(f"Request: method: ['{request.method}'], url: {request.url}, headers: {request.headers}, "
                 f"body: {request.body}")
    json_data = None
    try:
        cache_data = redis_instance.hgetall(str(item_id))
        if cache_data:
            logging.info(f'Fetching item from cache with id: {item_id}')
            result_dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in cache_data.items()}
            json_data = json.dumps(result_dict)
        else:
            query = 'SELECT * FROM items where itemid = :item_id'

            logging.info(f'Executing query: {query} to fetch item with id: {item_id}')
            res = db.execute(text(query), {'item_id': item_id}).fetchone()

            if res:
                logging.info(f'Caching item with id: {item_id}')
                redis_instance.hmset(str(item_id), mapping={'item_name': res.itemname, 'item_desc': res.itemdesc})

                json_data = json.dumps({'item_name': res.itemname, 'item_desc': res.itemdesc})

        if not json_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

        logging.info(f'Item found with id: {item_id}')
        response = responses.JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(json_data))

        logging.info(f"Request: method: ['{request.method}'], url: {request.url}, headers: {request.headers}, "
                     f"body: {request.body}:: Response: status_code = {response.status_code}, content = {response.body}")
        return response

    except Exception as e:
        response = responses.JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': str(e)})
        logging.error(f"Request: method: ['{request.method}'], url: {request.url}, headers: {request.headers}, "
                      f"body: {request.body}:: Response: status_code = {response.status_code}, content = {response.body}")
        return response


@router.put('/items/{item_id}')
async def update_item(item_id: str, request: Request, db: Session = Depends(get_db),
                      redis_instance: any = Depends(get_redis_pool)):
    logging.info(
        f"Request method: ['{request.method}'], url: {request.url}, headers: {request.headers}, body: {request.body}")
    try:
        query = 'SELECT * FROM items where itemid = :item_id'

        logging.info(f'Executing query: {query} to fetch item with id: {item_id}')
        res = db.execute(text(query), {'item_id': item_id}).fetchone()

        if res:
            data = await request.json()
            item_name = data.get('itemname')
            item_desc = data.get('itemdesc')

            query = 'UPDATE items SET itemname = :item_name, itemdesc = :item_desc where itemid = :item_id'

            logging.info(f'Executing query: {query} to update item with id: {item_id}')
            db.execute(text(query), {'item_id': item_id, 'item_name': item_name, 'item_desc': item_desc})
            db.commit()

            logging.info(f'Updating cached item with id: {item_id}')
            redis_instance.hmset(str(item_id), mapping={'item_name': res.itemname, 'item_desc': res.itemdesc})

            response = responses.JSONResponse(status_code=status.HTTP_200_OK,
                                              content={'item_name': item_name, 'item_desc': item_desc})
            logging.info(f"Request: method: ['{request.method}'], url: {request.url}, headers: {request.headers}, "
                         f"body: {request.body}:: Response: status_code = {response.status_code}, "
                         f"content = {response.body}")
            return response

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

    except Exception as e:
        response = responses.JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': str(e)})
        logging.error(f"Request: method: ['{request.method}'], url: {request.url}, headers: {request.headers}, "
                      f"body: {request.body}:: Response: status_code = {response.status_code}, content = {response.body}")
        return response


@router.delete('/items/{item_id}')
async def delete_item(item_id: str, request: Request, db: Session = Depends(get_db),
                      redis_instance: any = Depends(get_redis_pool)):
    logging.info(
        f"Request method: ['{request.method}'], url: {request.url}, headers: {request.headers}, body: {request.body}")
    try:
        query = 'SELECT * FROM items where itemid = :item_id'

        logging.info(f'Executing query: {query} to fetch item with id: {item_id}')
        res = db.execute(text(query), {'item_id': item_id}).fetchone()

        if res:
            query = 'DELETE FROM items where itemid = :item_id'

            logging.info(f'Executing query: {query} to delete item with id: {item_id}')
            db.execute(text(query), {'item_id': item_id})
            db.commit()

            logging.info(f'Deleting cached item with id: {item_id}')
            redis_instance.delete(str(item_id))

            response = responses.JSONResponse(status_code=status.HTTP_200_OK,
                                              content={'message': 'Item Deleted Successfully'})
            logging.info(f"Request: method: ['{request.method}'], url: {request.url}, headers: {request.headers}, "
                         f"body: {request.body}:: Response: status_code = {response.status_code}, "
                         f"content = {response.body}")
            return response

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

    except Exception as e:
        response = responses.JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': str(e)})
        logging.error(f"Request: method: ['{request.method}'], url: {request.url}, headers: {request.headers}, "
                      f"body: {request.body}:: Response: status_code = {response.status_code}, "
                      f"content = {response.body}")
        return response
