
import os
from rest_framework_simplejwt.tokens import RefreshToken
import random
from twilio.rest import Client

def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    

def generate_otp(self):

        # Step 1: Generate OTP
        self.otp = str(random.randint(100000, 999999))
        self.save()

        # Step 2: Twilio trial credentials
        account_sid = 'AC402d33242dda26263db81bca6c3094a3'
        auth_token = 'eb2befd348c0e5e07b6a828ef633d61b'
        twilio_number = '+12513172340'  # Your Twilio trial number

        # Step 3: Create client
        client = Client(account_sid, auth_token)

        # ✅ Step 4: Use self.phone_number if it's verified
        VERIFIED_NUMBERS = ['+919072253087']  # Add all verified numbers here

        if self.phone_number not in VERIFIED_NUMBERS:
            print(f"❌ {self.phone_number} is not verified in Twilio trial. SMS not sent.")
            return

        try:
            message = client.messages.create(
                body=f'Your OTP is {self.otp}',
                from_=twilio_number,
                to=self.phone_number  # Use the user's phone number
            )
            print("✅ OTP sent to", self.phone_number, "SID:", message.sid)
        except Exception as e:
            print("❌ Twilio error:", e)
            
            
            
  # def generate_otp(self):
    #     self.otp = str(random.randint(100000, 999999))
    #     self.save()
    
    
    # def generate_otp(self):
    #     self.otp = str(random.randint(100000, 999999))
    #     self.save()

    #     # Twilio Config
    #     account_sid = 'AC402d33242dda26263db81bca6c3094a3'
    #     auth_token = 'eb2befd348c0e5e07b6a828ef633d61b'
    #     twilio_number = '+12513172340'  
      
    #     client = Client(account_sid, auth_token)
    #     print(client , 'ottotottppp')

    #     try:
    #         message = client.messages.create(
    #             body=f'Your OTP is {self.otp}',
    #             from_=twilio_number,
    #             to=self.phone_number  # Make sure it's in +91xxxxxxxx format for India
    #         )
    #         print("OTP sent:", message.sid)
    #     except Exception as e:
    #         print("Twilio error:", e)
   
   
    
