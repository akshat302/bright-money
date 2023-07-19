from dateutil.relativedelta import relativedelta
from django.db.models import Sum

from loan_management_service.models import (EMIDetails, LoanInfo,
                                            UserInformation,
                                            UserTransactionInformation)


class UserInformationDbService:

    def __init__(self):
        self.user_information = UserInformation

    def get_user_by_uuid(self, user_uuid):
        return self.user_information.objects.filter(user_uuid=user_uuid).first()
    
    def create_user(self, )

class UserTransactionInformationDbService:

    def __init__(self):
        self.user_transaction_information = UserTransactionInformation

class LoanInformationDbService:

    def __init__(self):
        self.loan_information = LoanInfo
    
    def get_loan_information(self, loan_id):

        loan_information = self.loan_information.objects.filter(loan_id=loan_id).first()
        return loan_information

    def create_entry(self, user_uuid, loan_type, loan_amount, interest_rate, term_period):

        loan_info_model = self.loan_information.objects.create(user_uuid=user_uuid, loan_type=loan_type, loan_amount=loan_amount, interest_rate=interest_rate, term_period=term_period)
        return loan_info_model.loan_id  

class EMIDetailsDbService:

    def __init__(self):
        self.emi_details = EMIDetails

    def add_bulk(self, models):
        self.emi_details.objects.bulk_create(models)

    def save_emi_details(self, loan_id, emi_due, disbursement_date, term_period):

        emi_models = []
        for i in range(1, term_period+1):
            installment_date = (disbursement_date.replace(day=1) + relativedelta(months=i)).date()
            emi_model = self.emi_details(loan_id=loan_id, amount_due=emi_due, amount_paid=0, installment_date=installment_date)
            emi_models.append(emi_model)

        self.add_bulk(emi_models)
    
    def get_emi_details_by_loan_id(self, loan_id):

        emi_detail_objects = self.emi_details.objects.filter(loan_id=loan_id).all()
        return emi_detail_objects     
    
    def get_emi_details_by_installment_date(self, loan_id, installment_date):

        emi_details = self.emi_details.objects.filter(loan_id=loan_id, installment_date=installment_date).first()
        return emi_details

    def update_paid_amount(self, loan_id, amount, installment_date):
        self.emi_details.objects.filter(loan_id=loan_id, installment_date=installment_date).update(amount_paid=amount)

    def get_sum_of_paid_emis(self, loan_id):
        paid_emis_sum = self.emi_details.objects.filter(loan_id=loan_id,amount_due__gt=0, amount_paid__gt=0).aggregate(total_amount=Sum('amount_paid'))
        return paid_emis_sum['total_amount']

    def no_of_emis_paid(self, loan_id):
        return self.emi_details.objects.filter(loan_id=loan_id, amount_due__gt=0, amount_paid__gt=0).count()
    
    def update_due_amount(self, loan_id, amount):
        return self.emi_details.objects.filter(loan_id=loan_id, amount_due__gt=0, amount_paid=0).update(amount_due=amount)
    