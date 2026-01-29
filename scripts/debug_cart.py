#!/usr/bin/env python3
"""
Debug cart contents
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from workers.booklet_maker_worker.worker_body import BookletMakerWorker

def debug_cart():
    worker = BookletMakerWorker(ucm_connector=None)
    user_id = 'demo_user_123'
    context = {'user_id': user_id, 'current_step': 1}

    # Upload file
    response = worker._generate_response('{"filename": "training_manual.pdf", "size": 5242880}', [], context)
    print('Upload response preview:', response[:100] + '...')

    # Check order
    order = worker.order_manager.load_order(user_id, context.get('order_id'))
    print('Order ID:', order.get('order_id'))
    print('Cart items count:', len(order['cart']['items']))
    print('Cart total:', order['cart']['total'])
    print('Cart subtotal:', order['cart']['subtotal'])

    for item in order['cart']['items']:
        print(f'Item: {item["name"]} - ${item["price"]/100:.2f}')

if __name__ == "__main__":
    debug_cart()