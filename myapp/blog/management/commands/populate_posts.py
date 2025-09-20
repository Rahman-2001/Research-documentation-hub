from typing import Any
from django.core.management.base import BaseCommand
from django.db import connection
from blog.models import Post, Category
import random 


class Command(BaseCommand):  # Must be "Command" with capital C
    help = "This command inserts post data and resets ID counter"

    def handle(self, *args: Any, **options: Any):

        # Delete all existing data
        Post.objects.all().delete()

        # Reset AUTO_INCREMENT ID counter
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE blog_post AUTO_INCREMENT = 1;")

        titles = [
            "Smart Farming Technologies Transforming Indian Agriculture",
            "How Artificial Intelligence is Enhancing Crop Yields",
            "5G Connectivity to Boost Precision Farming",
            "The Rise of Vertical Farming in Urban Spaces",
            "Blockchain for Transparent and Fair Agriculture Supply Chains",
            "Climate-Resilient Crops for a Sustainable Future",
            "Drone Technology in Crop Monitoring and Spraying",
            "Organic Farming: Healthier Soil and Food",
            "Empowering Farmers Through Mobile Apps and e-Marketplaces",
            "Sustainable Irrigation Methods Saving Water in Agriculture",
            "What is OpenCV Library"
        ]
        contents = [
            "Smart farming uses sensors, drones, and IoT devices to collect real-time data from the field. This helps farmers make better decisions about irrigation, fertilization, and pest control, leading to higher yields and reduced costs.",
            "AI is playing a major role in modern agriculture by analyzing weather patterns, soil data, and crop health. Farmers can now predict diseases early, optimize their planting schedule, and reduce waste with machine learning tools.",
            "With the rollout of 5G networks, smart devices and machines on farms can communicate instantly. This enables better automation, live monitoring, and remote management of equipment, greatly improving efficiency in the field.",
            "Vertical farming uses stacked layers to grow crops in controlled environments. It saves space, reduces water usage by up to 90%, and provides fresh produce year-round in cities where traditional farming is difficult.",
            "Blockchain technology allows for secure tracking of agricultural products from farm to market. It ensures fair pricing, prevents fraud, and builds trust among farmers, suppliers, and consumers by recording every transaction.",
            "Scientists are developing new crop varieties that can survive extreme heat, droughts, and floods. These climate-resilient crops help farmers adapt to changing weather and ensure food security for the growing population.",
            "Drones can scan large farm areas quickly and provide detailed images of crop health. They are also used for precision spraying of fertilizers and pesticides, reducing labor costs and environmental impact.",
            "Organic farming avoids synthetic chemicals and promotes the use of compost, green manure, and natural pest control. This not only improves soil fertility but also produces healthier, chemical-free food for consumers.",
            "Digital platforms allow farmers to check crop prices, weather updates, and connect directly with buyers. These tools empower small-scale farmers to make informed decisions and access wider markets without middlemen.",
            "Drip and sprinkler irrigation systems deliver water directly to the roots, minimizing waste. These sustainable methods help conserve water, reduce energy use, and ensure better crop productivity even in dry regions.",
            "OpenCV (Open Source Computer Vision Library) is an open-source software toolkit for computer vision and machine learning tasks. Originally developed by Intel, it is now maintained by the OpenCV Foundation and a large community of contributors. OpenCV enables developers to process and analyze visual data such as images and videos with efficiency."
        ]
        img_urls = [
            "https://picsum.photos/id/1/800/400",
            "https://picsum.photos/id/2/800/400",
            "https://picsum.photos/id/3/800/400",
            "https://picsum.photos/id/4/800/400",
            "https://picsum.photos/id/5/800/400",
            "https://picsum.photos/id/6/800/400",
            "https://picsum.photos/id/7/800/400",
            "https://picsum.photos/id/8/800/400",
            "https://picsum.photos/id/9/800/400",
            "https://picsum.photos/id/10/800/400",
            "https://picsum.photos/id/11/800/400"
        ]

        categories = Category.objects.all()

        for title, content, img_url in zip(titles, contents, img_urls):
            category = random.choice(categories)
            Post.objects.create(title=title, content=content, img_url=img_url, category=category)

        self.stdout.write(self.style.SUCCESS("✅ Completed inserting data and reset ID counter!"))
