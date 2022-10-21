from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from linkedin.bot.messages import SendMessages
from linkedin.bot.outreach import Messages, get_message
from linkedin.bot.profile import Profiles, get_link
from linkedin.models import LinkedInProfile


# Create your views here.

class Testing(View):
    def get(self, request):
        response = {
            "message": "Sameer Kumar"
        }

        profile = Profiles()
        profile.run()
        profile.close_session()

        return JsonResponse(response)


class ListOfAllProfiles(View):
    @staticmethod
    def get(request):
        profiles = LinkedInProfile.objects.all()

        items = []
        for profile in profiles:
            items.append({
                "fullName": profile.fullName,
                "jobTitle": profile.jobTitle,
                "status": profile.status
            })

        response = {
            "count": len(items),
            "data": items
        }

        return JsonResponse(response)


print("1. Linked In Profile")
print("2. Send Message")
print("3. (Or any other) Exit")

choice = int(input("Enter choice: "))

if choice == 1:
    profile = Profiles()
    profile.run()
    profile.close_session()

elif choice == 2:
    send_message = SendMessages()
    send_message.run()
    send_message.close_session()

else:
    print("Exit.")
