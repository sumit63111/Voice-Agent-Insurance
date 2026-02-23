# import json
# import re
# from typing import List, Dict, Any
# from dataclasses import dataclass, asdict

# @dataclass
# class Chunk:
#     id: str
#     content: str
#     metadata: Dict[str, Any]
    
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "content": self.content,
#             "metadata": self.metadata
#         }

# class PolicyDocumentChunker:
#     def __init__(self):
#         self.chunks: List[Chunk] = []
#         self.chunk_counter = 0
        
#     def _generate_id(self, prefix: str) -> str:
#         self.chunk_counter += 1
#         return f"{prefix}_{self.chunk_counter:03d}"
    
#     def _clean_text(self, text: str) -> str:
#         """Clean extracted text"""
#         text = re.sub(r'\s+', ' ', text)
#         text = text.replace('HDFC ERGO', '').strip()
#         return text
    
#     def create_chunk(self, content: str, metadata: Dict) -> Chunk:
#         """Create a chunk with generated ID"""
#         prefix = metadata.get('section', 'GEN').replace('.', '_').replace(' ', '_')
#         chunk_id = self._generate_id(prefix)
        
#         return Chunk(
#             id=chunk_id,
#             content=self._clean_text(content),
#             metadata=metadata
#         )
    
#     def chunk_document(self) -> List[Dict]:
#         """Main method to chunk the entire policy document"""
        
#         # ========== SECTION A: DEFINITIONS ==========
#         self._chunk_standard_definitions()
#         self._chunk_specific_definitions()
        
#         # ========== SECTION B: BENEFITS ==========
#         self._chunk_base_coverages()
#         self._chunk_optional_coverages()
#         self._chunk_renewal_benefits()
        
#         # ========== SECTION C: WAITING PERIODS & EXCLUSIONS ==========
#         self._chunk_waiting_periods()
#         self._chunk_standard_exclusions()
#         self._chunk_specific_exclusions()
        
#         # ========== SECTION D & E: GENERAL TERMS ==========
#         self._chunk_general_terms()
        
#         # ========== ANNEXURES ==========
#         self._chunk_annexures()
        
#         return [chunk.to_dict() for chunk in self.chunks]
    
#     def _chunk_standard_definitions(self):
#         """Section A.1.1 - Standard Definitions (Def.1 to Def.43)"""
        
#         definitions = [
#             {
#                 "term": "Accident",
#                 "def_num": "Def.1",
#                 "content": "Accident means a sudden, unforeseen and involuntary event caused by external, visible and violent means.",
#                 "page": 2
#             },
#             {
#                 "term": "Any one illness",
#                 "def_num": "Def.2", 
#                 "content": "Any one illness means continuous period of illness and includes relapse within 45 days from the date of last consultation with the Hospital/Nursing Home where treatment was taken.",
#                 "page": 2
#             },
#             {
#                 "term": "AYUSH Hospital",
#                 "def_num": "Def.3",
#                 "content": "AYUSH Hospital is a healthcare facility wherein medical/surgical/para-surgical treatment procedures and interventions are carried out by AYUSH Medical Practitioner(s) comprising of any of the following: a) Central or State Government AYUSH Hospital; or b) Teaching hospital attached to AYUSH College recognized by the Central Government/Central Council of Indian Medicine/Central Council for Homeopathy; or c) AYUSH Hospital, standalone or co-located within in-patient healthcare facility of any recognized system of medicine, registered with the local authorities, wherever applicable, and is under the supervision of a qualified registered AYUSH Medical Practitioner and must comply with all the following criterion: i. Having at least 5 in-patient beds; ii. Having qualified AYUSH Medical Practitioner in charge round the clock; iii. Having dedicated AYUSH therapy sections as required and/or has equipped operation theatre where surgical procedures are to be carried out; iv. Maintaining daily records of the patients and making them accessible to the insurance company's authorized personnel.",
#                 "page": 2
#             },
#             {
#                 "term": "AYUSH Day Care Centre",
#                 "def_num": "Def.4",
#                 "content": "AYUSH Day Care Centre means and includes Community Health Centre (CHC), Primary Health Centre (PHC), Dispensary, Clinic, Polyclinic or any such health centre which is registered with the local authorities, wherever applicable and having facilities for carrying out treatment procedures and medical or surgical/para-surgical interventions or both under the supervision of registered AYUSH Medical Practitioner(s) on day care basis without in-patient services and must comply with all the following criterion: i. Having qualified registered AYUSH Medical Practitioner(s) in charge; ii. Having dedicated AYUSH therapy sections as required and/or has equipped operation theatre where surgical procedures are to be carried out; iii. Maintaining daily records of the patients and making them accessible to the insurance company's authorized personnel.",
#                 "page": 3
#             },
#             {
#                 "term": "Cashless facility",
#                 "def_num": "Def.5",
#                 "content": "Cashless facility means a facility extended by the insurer to the insured where the payments, of the costs of treatment undergone by the insured in accordance with the policy terms and conditions, are directly made to the network provider by the insurer to the extent preauthorization is obtained.",
#                 "page": 3
#             },
#             {
#                 "term": "Condition Precedent",
#                 "def_num": "Def.6",
#                 "content": "Condition Precedent means a policy term or condition upon which the Insurer's liability under the policy is conditional.",
#                 "page": 3
#             },
#             {
#                 "term": "Congenital Anomaly",
#                 "def_num": "Def.7",
#                 "content": "Congenital Anomaly means a condition which is present since birth, and which is abnormal with reference to form, structure or position. a) Internal Congenital Anomaly: Congenital anomaly which is not in the visible and accessible parts of the body. b) External Congenital Anomaly: Congenital anomaly which is in the visible and accessible parts of the body.",
#                 "page": 3
#             },
#             {
#                 "term": "Co-Payment",
#                 "def_num": "Def.8",
#                 "content": "Co-Payment means a cost sharing requirement under a health insurance policy that provides that the policyholder/insured will bear a specified percentage of the admissible claims amount. A co-payment does not reduce the Sum Insured.",
#                 "page": 3
#             },
#             {
#                 "term": "Cumulative Bonus",
#                 "def_num": "Def.9",
#                 "content": "Cumulative Bonus means any increase or addition in the Sum Insured granted by the insurer without an associated increase in premium.",
#                 "page": 3
#             },
#             {
#                 "term": "Day Care Centre",
#                 "def_num": "Def.10",
#                 "content": "Day Care Centre means any institution established for day care treatment of illness and/or injuries or a medical set-up with a hospital and which has been registered with the local authorities, wherever applicable, and is under the supervision of a registered and qualified medical practitioner AND must comply with all minimum criterion as under: i. has qualified nursing staff under its employment; ii. has qualified medical practitioner/s in charge; iii. has fully equipped operation theatre of its own where surgical procedures are carried out; iv. maintains daily records of patients and will make these accessible to the insurance company's authorized personnel.",
#                 "page": 3
#             },
#             {
#                 "term": "Day Care Treatment",
#                 "def_num": "Def.11",
#                 "content": "Day Care Treatment means those medical treatment, and/or surgical procedure which is i) undertaken under General or Local Anaesthesia in a hospital/day care centre in less than 24 hours because of technological advancement, and ii) which would have otherwise required hospitalization of more than 24 hours. Treatment normally taken on an out-patient basis is not included in the scope of this definition.",
#                 "page": 4
#             },
#             {
#                 "term": "Deductible",
#                 "def_num": "Def.12",
#                 "content": "Deductible means a cost-sharing requirement under a health insurance policy that provides that the insurer will not be liable for a specified rupee amount in case of indemnity policies and for a specified number of days/hours in case of hospital cash policies which will apply before any benefits are payable by the insurer. A deductible does not reduce the Sum Insured. The deductible is separate from any Aggregate Deductible that may be in-force and applicable under the Policy, as specified in the Policy Schedule.",
#                 "page": 4
#             },
#             {
#                 "term": "Dental Treatment",
#                 "def_num": "Def.13",
#                 "content": "Dental Treatment means a treatment related to teeth or structures supporting teeth including examinations, fillings (where appropriate), crowns, extractions and surgery.",
#                 "page": 4
#             },
#             {
#                 "term": "Disclosure of information norm",
#                 "def_num": "Def.14",
#                 "content": "Disclosure of information norm means the policy shall be void and all premium paid hereon shall be forfeited to the Company in the event of misrepresentation, mis-description or non-disclosure of any material fact.",
#                 "page": 4
#             },
#             {
#                 "term": "Domiciliary Hospitalization",
#                 "def_num": "Def.15",
#                 "content": "Domiciliary Hospitalization means medical treatment for an illness/disease/injury which in the normal course would require care and treatment at a hospital but is actually taken while confined at home under any of the following circumstances: i. the condition of the patient is such that he/she is not in a condition to be removed to a hospital, or ii. the patient takes treatment at home on account of non-availability of room in a hospital.",
#                 "page": 4
#             },
#             {
#                 "term": "Emergency Care",
#                 "def_num": "Def.16",
#                 "content": "Emergency Care means management for an illness or injury which results in symptoms which occur suddenly and unexpectedly, and requires immediate care by a medical practitioner to prevent death or serious long term impairment of the insured person's health.",
#                 "page": 4
#             },
#             {
#                 "term": "Grace Period",
#                 "def_num": "Def.17",
#                 "content": "Grace Period means the specified period of time, immediately following the premium due date during which premium payment can be made to renew or continue a policy in force without loss of continuity benefits pertaining to waiting periods and coverage of pre-existing diseases. Coverage need not be available during the period for which no premium is received. The grace period for payment of the premium for all types of insurance policies shall be: fifteen days where premium payment mode is monthly and thirty days in all other cases. Provided the insurers shall offer coverage during the grace period, if the premium is paid in instalments during the policy period.",
#                 "page": 4
#             },
#             {
#                 "term": "Hospital",
#                 "def_num": "Def.18",
#                 "content": "Hospital means any institution established for in-patient care and day care treatment of Illness and/or injuries and which has been registered as a hospital with the local authorities under the Clinical Establishments (Registration and Regulation) Act 2010 or under the enactments specified under the Schedule of Section 56(1) of the said act or complies with all minimum criteria as under: i) has qualified nursing staff under its employment round the clock; ii) has at least 10 in-patient beds in towns having a population of less than 10,00,000 and at least 15 in-patient beds in all other places; iii) has qualified medical practitioner(s) in charge round the clock; iv) has a fully equipped operation theatre of its own where surgical procedures are carried out; v) maintains daily records of patients and make these accessible to the insurance company's authorized personnel.",
#                 "page": 5
#             },
#             {
#                 "term": "Hospitalization",
#                 "def_num": "Def.19",
#                 "content": "Hospitalization means admission in a Hospital for a minimum period of 24 consecutive 'Inpatient Care' hours except for specified procedures/treatments, where such admission could be for a period of less than 24 consecutive hours.",
#                 "page": 5
#             },
#             {
#                 "term": "Illness",
#                 "def_num": "Def.20",
#                 "content": "Illness means a sickness or a disease or pathological condition leading to the impairment of normal physiological function and requires medical treatment. (a) Acute condition – Acute condition means is a disease, illness or injury that is likely to respond quickly to treatment which aims to return the person to his or her state of health immediately before suffering the disease/illness/injury which leads to full recovery. (b) Chronic condition – A chronic condition is defined as a disease, illness, or injury that has one or more of the following characteristics: 1. it needs ongoing or long-term monitoring through consultations, examinations, check-ups, and/or tests; 2. it needs ongoing or long-term control or relief of symptoms; 3. it requires rehabilitation for the patient or for the patient to be specially trained to cope with it; 4. it continues indefinitely; 5. it recurs or is likely to recur.",
#                 "page": 5
#             },
#             {
#                 "term": "Injury",
#                 "def_num": "Def.21",
#                 "content": "Injury means accidental physical bodily harm excluding illness or disease solely and directly caused by external, violent and visible and evident means which is verified and certified by a Medical Practitioner.",
#                 "page": 5
#             },
#             {
#                 "term": "Inpatient Care",
#                 "def_num": "Def.22",
#                 "content": "Inpatient Care means treatment for which the insured person has to stay in a hospital for more than 24 hours for a covered condition.",
#                 "page": 5
#             },
#             {
#                 "term": "Intensive Care Unit",
#                 "def_num": "Def.23",
#                 "content": "Intensive Care Unit means an identified section, ward or wing of a hospital which is under the constant supervision of a dedicated medical practitioner(s), and which is specially equipped for the continuous monitoring and treatment of patients who are in a critical condition, or require life support facilities and where the level of care and supervision is considerably more sophisticated and intensive than in the ordinary and other wards.",
#                 "page": 5
#             },
#             {
#                 "term": "ICU Charges",
#                 "def_num": "Def.24",
#                 "content": "ICU (Intensive Care Unit) Charges means the amount charged by a Hospital towards ICU expenses which shall include the expenses for ICU bed, general medical support services provided to any ICU patient including monitoring devices, critical care nursing and intensivist charges.",
#                 "page": 6
#             },
#             {
#                 "term": "Medical Advice",
#                 "def_num": "Def.25",
#                 "content": "Medical Advice means any consultation or advice from a Medical Practitioner including the issuance of any prescription or follow-up consultation.",
#                 "page": 6
#             },
#             {
#                 "term": "Medical Expenses",
#                 "def_num": "Def.26",
#                 "content": "Medical Expenses means those expenses that an Insured Person has necessarily and actually incurred for medical treatment on account of Illness or Accident on the advice of a Medical Practitioner, as long as these are no more than would have been payable if the Insured Person had not been insured and no more than other hospitals or doctors in the same locality would have charged for the same medical treatment.",
#                 "page": 6
#             },
#             {
#                 "term": "Medical Practitioner",
#                 "def_num": "Def.27",
#                 "content": "Medical Practitioner means a person who holds a valid registration from the Medical Council of any State or Medical Council of India or Council for Indian Medicine or for Homeopathy set up by the Government of India or a State Government and is thereby entitled to practice medicine within its jurisdiction; and is acting within the scope and jurisdiction of license. Medical Practitioner who is sharing the same residence as the Insured Person and is a Family Member of the Insured Person are not considered as Medical Practitioner under the scope of this Policy. Medical Practitioner (Definition applicable for the treatment taken outside India) means a licensed medical practitioner acting within the scope of his license and who holds a degree of a recognized institution and is registered by the Authorized Medical Council of the respective country.",
#                 "page": 6
#             },
#             {
#                 "term": "Medically Necessary Treatment",
#                 "def_num": "Def.28",
#                 "content": "Medically Necessary Treatment means any treatment, test, medication, or stay in hospital or part of stay in hospital which: i) is required for the medical management of the illness or injury suffered by the insured; ii) must not exceed the level of care necessary to provide safe, adequate and appropriate medical care in scope, duration or intensity; iii) must have been prescribed by a medical practitioner; iv) must conform to the professional standards widely accepted in international medical practice or by the medical community in India.",
#                 "page": 6
#             },
#             {
#                 "term": "Migration",
#                 "def_num": "Def.29",
#                 "content": "Migration means a facility provided to policyholders (including all members under family cover and group policies), to transfer the credits gained for pre-existing diseases and specific waiting periods from one health insurance policy to another with the same insurer.",
#                 "page": 6
#             },
#             {
#                 "term": "Network Provider",
#                 "def_num": "Def.30",
#                 "content": "Network Provider means hospitals or health care providers enlisted by an insurer, TPA or jointly by an Insurer and TPA to provide medical services to an insured by a cashless facility.",
#                 "page": 6
#             },
#             {
#                 "term": "Non-Network Provider",
#                 "def_num": "Def.31",
#                 "content": "Non-Network Provider means any hospital, day care centre or other provider that is not part of the network.",
#                 "page": 6
#             },
#             {
#                 "term": "Notification of Claim",
#                 "def_num": "Def.32",
#                 "content": "Notification of Claim means the process of intimating a claim to the insurer or TPA through any of the recognized modes of communication.",
#                 "page": 7
#             },
#             {
#                 "term": "OPD Treatment",
#                 "def_num": "Def.33",
#                 "content": "OPD Treatment means the one in which the Insured visits a clinic/hospital or associated facility like a consultation room for diagnosis and treatment based on the advice of a Medical Practitioner. The Insured is not admitted as a day care patient or in-patient.",
#                 "page": 7
#             },
#             {
#                 "term": "Portability",
#                 "def_num": "Def.34",
#                 "content": "Portability means a facility provided to the health insurance policyholders (including all members under family cover), to transfer the credits gained for, pre-existing diseases and specific waiting periods from one insurer to another insurer.",
#                 "page": 7
#             },
#             {
#                 "term": "Pre-Existing Disease",
#                 "def_num": "Def.35",
#                 "content": "Pre-Existing Disease means any condition, ailment, injury or disease: a) that is/are diagnosed by a physician not more than 36 months prior to the date of commencement of the policy issued by the insurer; or b) for which medical advice or treatment was recommended by, or received from, a physician, not more than 36 months prior to the date of commencement of the policy.",
#                 "page": 7
#             },
#             {
#                 "term": "Pre-hospitalization Medical Expenses",
#                 "def_num": "Def.36",
#                 "content": "Pre-hospitalization Medical Expenses means Medical Expenses incurred during pre-defined number of days preceding the hospitalization of the Insured Person, provided that: i. Such Medical Expenses are incurred for the same condition for which the Insured Person's Hospitalization was required, and ii. The In-patient Hospitalization claim for such Hospitalization is admissible by the Insurance Company.",
#                 "page": 7
#             },
#             {
#                 "term": "Post-hospitalization Medical Expenses",
#                 "def_num": "Def.37",
#                 "content": "Post-hospitalization Medical Expenses means Medical Expenses incurred during predefined number of days immediately after the insured person is discharged from the hospital provided that: i. Such Medical Expenses are for the same condition for which the insured person's hospitalization was required, and ii. The inpatient hospitalization claim for such hospitalization is admissible by the insurance Company.",
#                 "page": 7
#             },
#             {
#                 "term": "Qualified Nurse",
#                 "def_num": "Def.38",
#                 "content": "Qualified Nurse means a person who holds a valid registration from the Nursing Council of India or the Nursing Council of any state in India.",
#                 "page": 7
#             },
#             {
#                 "term": "Reasonable and Customary Charges",
#                 "def_num": "Def.39",
#                 "content": "Reasonable and Customary Charges means the charges for services or supplies, which are the standard charges for a specific provider and consistent with the prevailing charges in the geographical area for identical or similar services, taking into account the nature of illness/injury involved.",
#                 "page": 7
#             },
#             {
#                 "term": "Renewal",
#                 "def_num": "Def.40",
#                 "content": "Renewal means the terms on which the contract of insurance can be renewed on mutual consent with a provision of grace period for treating the renewal continuous for the purpose of gaining credit for pre-existing diseases, time-bound exclusions and for all waiting periods.",
#                 "page": 7
#             },
#             {
#                 "term": "Room Rent",
#                 "def_num": "Def.41",
#                 "content": "Room Rent means the amount charged by a Hospital towards Room and Boarding expenses and shall include the associated medical expenses.",
#                 "page": 7
#             },
#             {
#                 "term": "Surgery or Surgical Procedure",
#                 "def_num": "Def.42",
#                 "content": "Surgery or Surgical Procedure means manual and/or operative procedure(s) required for treatment of an illness or injury, correction of deformities and defects, diagnosis and cure of diseases, relief from suffering and prolongation of life, performed in a hospital or day care centre by a medical practitioner.",
#                 "page": 8
#             },
#             {
#                 "term": "Unproven/Experimental Treatment",
#                 "def_num": "Def.43",
#                 "content": "Unproven/Experimental Treatment means the treatment including drug experimental therapy which is not based on established medical practice in India, is a treatment experimental or unproven.",
#                 "page": 8
#             }
#         ]
        
#         for d in definitions:
#             chunk = self.create_chunk(
#                 content=f"{d['def_num']}. {d['term']}: {d['content']}",
#                 metadata={
#                     "section": "A.1.1",
#                     "subsection": "Standard Definitions",
#                     "term": d['term'],
#                     "def_number": d['def_num'],
#                     "type": "definition",
#                     "page": d['page'],
#                     "category": "standard"
#                 }
#             )
#             self.chunks.append(chunk)
    
#     def _chunk_specific_definitions(self):
#         """Section A.1.2 - Specific Definitions (Def.1 to Def.30)"""
        
#         specific_defs = [
#             {
#                 "term": "Adventurous/Hazardous Sports",
#                 "def_num": "Def.1",
#                 "content": "Adventurous/Hazardous Sports means any sport or activity involving physical exertion and skill in which an Insured Person participates or competes for entertainment or as part of his profession whether he/she is trained or untrained.",
#                 "page": 8
#             },
#             {
#                 "term": "Age",
#                 "def_num": "Def.2",
#                 "content": "Age means completed years on last birthday as on Commencement Date.",
#                 "page": 8
#             },
#             {
#                 "term": "Aggregate Deductible",
#                 "def_num": "Def.3",
#                 "content": "Aggregate Deductible refers to a cost-sharing agreement between the Insurer and the Insured. The Insured agrees to bear a self-opted amount known as 'Aggregate Deductible' once during each Policy Year post which the Insurer's liability under the Policy shall commence for that Policy Year. The Aggregate Deductible does not reduce the Sum Insured.",
#                 "page": 8
#             },
#             {
#                 "term": "Ambulance",
#                 "def_num": "Def.4",
#                 "content": "Ambulance means a motor vehicle operated by a licenced/authorised service provider and equipped for the transport and paramedical treatment of the person requiring medical attention.",
#                 "page": 8
#             },
#             {
#                 "term": "Associated Medical Expenses",
#                 "def_num": "Def.5",
#                 "content": "Associated Medical Expenses means Consultation fees, charges on Operation theatre, surgical appliances & nursing, and expenses on Anesthesia, blood, oxygen incurred during Hospitalization of the Insured Person which vary based on the room category occupied by the insured person whilst undergoing treatment in some of the hospitals. If Policy Holder chooses a higher room category above the eligibility defined in Policy Schedule, then proportionate deduction will apply on the Associated Medical Expenses in addition to the difference in room rent. Such associated medical expenses do not include Cost of pharmacy and consumables, Cost of implants and medical devices and Cost of diagnostics. Proportionate deduction shall not be applicable to 'ICU Charges'.",
#                 "page": 8
#             },
#             {
#                 "term": "AYUSH Treatment",
#                 "def_num": "Def.6",
#                 "content": "AYUSH Treatment refers to the medical and/or hospitalisation treatments given under Ayurveda, Yoga and Naturopathy, Unani, Siddha and Homeopathy systems of medicines.",
#                 "page": 8
#             },
#             {
#                 "term": "Bank Rate",
#                 "def_num": "Def.7",
#                 "content": "Bank Rate means the rate fixed by the Reserve Bank of India (RBI) at the beginning of the financial year, which shall be applied depending on the year in which a claim is made.",
#                 "page": 8
#             },
#             {
#                 "term": "Base/Basic Sum Insured",
#                 "def_num": "Def.8",
#                 "content": "Base/Basic Sum Insured means the limit opted at the time of inception or modified at the time of renewal whichever is later. It forms a part of the Sum insured for a given Policy Year. It is on per Policy Year basis. In case of Individual Policies Base Sum Insured shall be on per Insured Person basis. In case of Family Floater policies, a common Base Sum Insured shall be available on a floating basis amongst all the Insured Persons.",
#                 "page": 8
#             },
#             {
#                 "term": "Break in policy",
#                 "def_num": "Def.9",
#                 "content": "Break in policy means the period of gap that occurs at the end of the existing policy term/instalment premium due date, when the premium due for renewal on a given policy or instalment premium due is not paid on or before the premium renewal date or grace period.",
#                 "page": 9
#             },
#             {
#                 "term": "Biological Attack or Weapons",
#                 "def_num": "Def.10",
#                 "content": "Biological Attack or Weapons means the emission, discharge, dispersal, release or escape of any pathogenic (disease producing) micro-organisms and/or biologically produced toxins (including genetically modified organisms and chemically synthesized toxins) which are capable of causing any Illness, incapacitating disablement or death.",
#                 "page": 9
#             },
#             {
#                 "term": "Chemical attack or weapons",
#                 "def_num": "Def.11",
#                 "content": "Chemical attack or weapons means the emission, discharge, dispersal, release or escape of any solid, liquid or gaseous chemical compound which, when suitably distributed, is capable of causing any Illness, incapacitating disablement or death.",
#                 "page": 9
#             },
#             {
#                 "term": "Commencement Date",
#                 "def_num": "Def.12",
#                 "content": "Commencement Date means the date of commencement of insurance coverage under the Policy as specified in the Policy Schedule.",
#                 "page": 9
#             },
#             {
#                 "term": "Family Members",
#                 "def_num": "Def.13",
#                 "content": "Family Members means any one or more of the following family members of the Insured Person: i. Legally wedded spouse; ii. Parents and parents-in-law; iii. Dependent Children (i.e. natural or legally adopted) between the Age 90 days to Age 25 years. If the child above 18 years of Age is financially independent, he or she shall be ineligible for coverage under this Policy in the subsequent renewals.",
#                 "page": 9
#             },
#             {
#                 "term": "Home",
#                 "def_num": "Def.14",
#                 "content": "Home means the Insured Person's place of permanent residence as specified in the Policy Schedule.",
#                 "page": 9
#             },
#             {
#                 "term": "Insured Person",
#                 "def_num": "Def.15",
#                 "content": "Insured Person means persons named in the Policy Schedule who are insured under the Policy and in respect of whom the applicable premium has been received in full.",
#                 "page": 9
#             },
#             {
#                 "term": "Life threatening situation",
#                 "def_num": "Def.16",
#                 "content": "Life threatening situation shall mean a serious medical condition or symptom resulting from Injury or Illness which is not Pre-Existing Disease, which arises suddenly and unexpectedly, and requires immediate care and treatment by a Medical Practitioner, generally received within 24 hours of onset to avoid jeopardy to life or serious long term impairment of the Insured Person's health, until stabilisation at which time this medical condition or symptom is not considered an Emergency.",
#                 "page": 9
#             },
#             {
#                 "term": "Material Facts",
#                 "def_num": "Def.17",
#                 "content": "Material Facts means all relevant information sought by the Company in the Proposal Form and other connected documents to enable it to take informed decision in the context of underwriting the Policy.",
#                 "page": 9
#             },
#             {
#                 "term": "Non-instalment Premium Payment",
#                 "def_num": "Def.18",
#                 "content": "Non-instalment Premium Payment refers to payment of premium for the entire policy period made in advance as a single payment.",
#                 "page": 9
#             },
#             {
#                 "term": "Policy",
#                 "def_num": "Def.19",
#                 "content": "Policy means these Policy wordings, the Policy Schedule and any applicable endorsements or extensions attaching to or forming part thereof, as amended from time to time, and shall be read together. The Policy contains details of the extent of cover available to the Insured Person, applicable exclusions and the terms & conditions applicable under the Policy.",
#                 "page": 9
#             },
#             {
#                 "term": "Policy Period",
#                 "def_num": "Def.20",
#                 "content": "Policy Period means the period between the Commencement Date and either the Expiry Date specified in the Policy Schedule or the date of cancellation of this Policy, whichever is earlier.",
#                 "page": 10
#             },
#             {
#                 "term": "Policyholder",
#                 "def_num": "Def.21",
#                 "content": "Policyholder means person who has proposed the Policy and in whose name the Policy is issued.",
#                 "page": 10
#             },
#             {
#                 "term": "Policy Schedule",
#                 "def_num": "Def.22",
#                 "content": "Policy Schedule means the Policy Schedule attached to and forming part of this Policy specifying the details of the Insured Persons, the Sum Insured, the Policy Period and the Sublimits to which benefits under the Policy are subject to, including any annexures and/or endorsements, made to or on it from time to time, and if more than one, then the latest in time.",
#                 "page": 10
#             },
#             {
#                 "term": "Policy Year",
#                 "def_num": "Def.23",
#                 "content": "Policy Year means a period of twelve months beginning from the Commencement Date and ending on the last day of such twelve-month period. For the purpose of subsequent years, Policy Year shall mean a period of twelve months commencing from the end of the previous Policy Year and lapsing on the last day of such twelve-month period, till the Expiry Date, as specified in the Policy Schedule.",
#                 "page": 10
#             },
#             {
#                 "term": "Preventive Health Check-up",
#                 "def_num": "Def.24",
#                 "content": "Preventive Health Check-up means a package of medical test(s) undertaken for general assessment of health status, excluding any diagnostic or investigative medical tests for evaluation of Illness or a condition.",
#                 "page": 10
#             },
#             {
#                 "term": "E-Opinion for Critical Illness",
#                 "def_num": "Def.25",
#                 "content": "E-Opinion for Critical Illness means a procedure where by upon request of the Insured Person, an independent Medical Practitioner reviews and opines on the treating Medical Practitioner's recommendation as to care and treatment of the Insured Person by reviewing Insured Person's medical status and history. Such an opinion shall not be deemed to substitute the Insured Person's physical visit or consultation to an independent Medical Practitioner.",
#                 "page": 10
#             },
#             {
#                 "term": "Shared Accommodation OR Shared Room category",
#                 "def_num": "Def.26",
#                 "content": "Shared Accommodation OR Shared Room category means a room in a Hospital with double occupancy having shared washroom. This room does not include kitchen/dining area.",
#                 "page": 10
#             },
#             {
#                 "term": "Single Private Room",
#                 "def_num": "Def.27",
#                 "content": "Single Private Room means an air-conditioned room in a Hospital where a single patient is accommodated and which has an attached toilet (lavatory and bath). Such room type shall be the most economical of all accommodations available as a single AC room in that Hospital.",
#                 "page": 10
#             },
#             {
#                 "term": "Sub-limit",
#                 "def_num": "Def.28",
#                 "content": "Sub-limit means a cost sharing requirement under a health insurance policy in which an insurer would not be liable to pay any amount in excess of the pre-defined limit. The Sub-limit as applicable under the Policy is specified in the Policy Schedule against the relevant Cover in force under the Policy.",
#                 "page": 10
#             },
#             {
#                 "term": "Sum Insured",
#                 "def_num": "Def.29",
#                 "content": "Sum Insured means the aggregate limit of indemnity consisting of the Base Sum Insured, Cumulative Bonus, Plus Benefit, Secure Benefit and Automatic Restore Benefit (provided that these covers are in force for the Insured Person). Sum Insured represents the maximum, total and cumulative liability of the Company for any and all claims made under the Policy, in respect of that Insured Person (on Individual basis) or all Insured Persons (on Floater basis) during the Policy Year.",
#                 "page": 10
#             },
#             {
#                 "term": "Waiting Period",
#                 "def_num": "Def.30",
#                 "content": "Waiting Period means a period from the inception of this Policy during which specified diseases/treatments are not covered. On completion of the Waiting Period, diseases/treatments shall be covered provided the Policy has been continuously renewed without any break.",
#                 "page": 10
#             }
#         ]
        
#         for d in specific_defs:
#             chunk = self.create_chunk(
#                 content=f"{d['def_num']}. {d['term']}: {d['content']}",
#                 metadata={
#                     "section": "A.1.2",
#                     "subsection": "Specific Definitions",
#                     "term": d['term'],
#                     "def_number": d['def_num'],
#                     "type": "definition",
#                     "page": d['page'],
#                     "category": "specific"
#                 }
#             )
#             self.chunks.append(chunk)
    
#     def _chunk_base_coverages(self):
#         """Section B.1 - Base Coverages"""
        
#         base_coverages = [
#             {
#                 "section_id": "B.1.1",
#                 "title": "Hospitalization Expenses",
#                 "content": "The Company shall indemnify Medical Expenses necessarily incurred by the Insured Person for Hospitalization of the Insured Person during the Policy Year due to Illness or Injury, up to the Sum Insured specified in the Policy Schedule for: a) Room Rent, boarding, nursing expenses as provided by the Hospital/Nursing Home. Room rent limit shall be 'At Actuals' unless otherwise specified in the Policy Schedule. b) Intensive Care Unit (ICU)/Intensive Cardiac Care Unit (ICCU) expenses. ICU limit (including ICCU) for bed charges shall be 'At Actuals' unless otherwise specified in the Policy Schedule. c) Surgeon, anaesthetist, Medical Practitioner, consultants, specialist Fees during Hospitalization forming part of Hospital bill. d) Investigative treatments and diagnostic procedures directly related to Hospitalization. e) Medicines and drugs prescribed in writing by Medical Practitioner. f) Intravenous fluids, blood transfusion, surgical appliances, allowable consumables and/or enteral feedings. Operation theatre charges. g) The cost of prosthetics and other devices or equipment, if implanted internally during Surgical Procedure.",
#                 "page": 11,
#                 "plans": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Lite", "Optima Secure Global Plus"]
#             },
#             {
#                 "section_id": "B.1.1.1",
#                 "title": "Other Expenses - Hospitalization",
#                 "content": "Other Expenses covered under Hospitalization: i. Expenses incurred on road Ambulance if the Insured Person is required to be transferred to the nearest Hospital for Emergency Care or from one Hospital to another Hospital or from Hospital to Home (within same city) following Hospitalization. ii. In patient Care Dental Treatment, necessitated due to disease or Injury. iii. Plastic Surgery, necessitated due to Injury. iv. All Day Care Treatment. Notes: i. Expenses of Hospitalization for a minimum period of 24 consecutive hours only shall be admissible. However, the time limit shall not apply in respect of Day Care Treatment. ii. The Hospitalization must be for Medically Necessary Treatment, and prescribed in writing by Medical Practitioner. iii. Proportionate deduction on Room Rent: In case the Insured Person is admitted in a room that exceeds the category/limit stipulated in the Policy Schedule, the reimbursement/payment of Room Rent charges including all Associated Medical Expenses incurred at Hospital shall be effected in the same proportion as the admissible rate per day bears to the actual rate per day of Room Rent charges. This condition is not applicable in respect of Hospitals where differential billing for Associated Medical Expenses is not followed based on Room Rent. In case the Insured Person is admitted in an ICU/ICCU room that exceeds the category/limit stipulated in the Policy Schedule then Proportionate deduction as stated above shall only apply on ICU/ICCU room charges for the days Insured Person was admitted in ICU/ICCU. Proportionate deduction will not apply for Associated Medical expenses incurred during the days Insured Person was admitted in ICU/ICCU.",
#                 "page": 11,
#                 "plans": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Lite", "Optima Secure Global Plus"]
#             },
#             {
#                 "section_id": "B.1.2",
#                 "title": "Home Health Care",
#                 "content": "The Company shall indemnify the Medical Expenses incurred by the Insured Person on availing treatment at Home during the Policy Year, if prescribed in writing by the treating Medical Practitioner, provided that: a. The treatment in normal course would require In-patient Care at a Hospital, and be admissible under Section B-1.1 (Hospitalization Expenses). b. The treatment is pre-authorized by the Company as per procedure given under Claims Procedure - Section E-1. c. Records of the treatment administered, duly signed by the treating Medical Practitioner, are maintained for each day of the Home Health Care. This Cover is not available on reimbursement basis.",
#                 "page": 12,
#                 "plans": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Secure Global Plus"],
#                 "geography": "India only"
#             },
#             {
#                 "section_id": "B.1.3",
#                 "title": "Domiciliary Hospitalization",
#                 "content": "The Company shall indemnify the Medical Expenses incurred during the Policy Year on Domiciliary Hospitalization of the Insured Person prescribed in writing by treating Medical Practitioner, provided that: a. the condition of the Insured Person is such that he/she could not be removed/admitted to a Hospital, or b. the Medically Necessary Treatment is taken at Home on account of non-availability of room in a hospital.",
#                 "page": 12,
#                 "plans": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Secure Global Plus"],
#                 "geography": "India only"
#             },
#             {
#                 "section_id": "B.1.4",
#                 "title": "AYUSH Treatment",
#                 "content": "The Company shall indemnify the Medical Expenses incurred by the Insured Person only for Inpatient Care under Ayurveda, Yoga and Naturopathy, Unani, Siddha and Homeopathy systems of medicines during each Policy Year up to the Sub-limit specified against this Cover in the Policy Schedule, in any AYUSH Hospital.",
#                 "page": 12,
#                 "plans": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Lite", "Optima Secure Global Plus"]
#             },
#             {
#                 "section_id": "B.1.5",
#                 "title": "Pre-Hospitalization Expenses",
#                 "content": "The Company shall indemnify the Pre-Hospitalization Medical Expenses incurred by the Insured Person only if the same is related to an admissible Hospitalization under Section B-1.1 (Hospitalization Expenses). Such expenses shall be indemnified if the same were incurred upto 60 days unless otherwise specified in the Policy Schedule, immediately prior to the date of admission.",
#                 "page": 12,
#                 "plans": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Secure Global Plus"],
#                 "duration_days": 60,
#                 "optima_lite_days": 30
#             },
#             {
#                 "section_id": "B.1.6",
#                 "title": "Post-Hospitalization Expenses",
#                 "content": "The Company shall indemnify the Post-Hospitalization Medical Expenses incurred by the Insured Person only if the same is related to an admissible Hospitalization under Section B-1.1 (Hospitalization Expenses). Such expenses shall be indemnified if the same were incurred upto 180 days unless otherwise specified in the Policy Schedule, immediately post the date of discharge from the Hospital.",
#                 "page": 13,
#                 "plans": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Secure Global Plus"],
#                 "duration_days": 180,
#                 "optima_lite_days": 60
#             },
#             {
#                 "section_id": "B.1.7",
#                 "title": "Organ Donor Expenses",
#                 "content": "The Company shall indemnify the Medical Expenses covered under Section B-1.1 (Hospitalization Expenses) which are incurred by the Insured Person during the Policy Year towards the organ donor's Hospitalization for harvesting of the donated organ where an Insured Person is the recipient, subject to the following conditions: a. The organ donor is any person whose organ has been made available in accordance and in compliance with The Transplantation of Human Organ (amendment) Act, 2011, Transplantation of Human Organs and Tissues Rules, 2014 and other applicable laws and/or regulations. b. Recipient Insured Person's claim under Section B-1.1 (Hospitalization Expenses) is admissible under the Policy. c. Expenses listed below are excluded from this Cover: i. The organ donor's Pre-Hospitalization Expenses and Post-Hospitalization Expenses. ii. Expenses related to organ transportation or preservation. iii. Any other Medical Expenses or Hospitalization consequent to the organ donation.",
#                 "page": 13,
#                 "plans": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Lite", "Optima Secure Global Plus"]
#             },
#             {
#                 "section_id": "B.1.8",
#                 "title": "Cumulative Bonus (CB)",
#                 "content": "On Renewal of this Policy with the Company without a break, a sum equal to 10% (unless otherwise specified in the policy schedule) of the Base Sum Insured of the expiring Policy shall be provided as CB irrespective of any claims and shall be available under the Renewed Policy subject to conditions: a. In case where the Policy is on individual basis, the CB shall be added and available individually to the Insured Person. b. In case where the Policy is on floater basis, the CB shall be added and available to the family on floater basis. c. CB shall be available only if the Policy is renewed/premium paid within the Grace Period. d. If expiring policy has CB and is renewed on floater basis, CB carried forward shall be the lowest one applicable among all Insured Persons. e. In case of floater policies split, CB shall be apportioned proportionately. f. If Sum Insured reduced at Renewal, CB reduced proportionately. g. If Sum Insured increased at Renewal, CB calculated on last completed Policy Year Sum Insured. h. For multi-year policies, CB credited post completion of each Policy Year. i. New Insured Persons eligible as per Renewal terms. j. CB available only if Cover specified in Policy Schedule. k. CB percentage and maximum accrual limit as specified in Policy Schedule. Applicable to 'Optima Suraksha', 'Optima Lite' and 'Optima Select' plans.",
#                 "page": 13,
#                 "applicable_plans": ["Optima Suraksha", "Optima Lite", "Optima Select"],
#                 "percentage": "10%",
#                 "max_accrual": "100%"
#             }
#         ]
        
#         for coverage in base_coverages:
#             chunk = self.create_chunk(
#                 content=f"{coverage['section_id']}. {coverage['title']}: {coverage['content']}",
#                 metadata={
#                     "section": "B.1",
#                     "subsection": coverage['section_id'],
#                     "title": coverage['title'],
#                     "type": "base_coverage",
#                     "page": coverage['page'],
#                     "plans": coverage.get('plans', []),
#                     "geography": coverage.get('geography', 'India'),
#                     "duration_days": coverage.get('duration_days'),
#                     "optima_lite_variant": coverage.get('optima_lite_days')
#                 }
#             )
#             self.chunks.append(chunk)
    
#     def _chunk_optional_coverages(self):
#         """Section B.2 - Optional Coverages"""
        
#         optional_coverages = [
#             {
#                 "section_id": "B.2.1",
#                 "title": "Emergency Air Ambulance",
#                 "content": "The Company shall indemnify expenses incurred by the Insured Person during the Policy Year towards Ambulance transportation in an airplane or helicopter for Emergency Care which requires immediate and rapid Ambulance transportation that ground transportation cannot provide from the site of first occurrence of the Illness or Accident to the nearest Hospital. Maximum of Sum Insured as specified in Policy Schedule. Conditions: a. Advised in writing by Medical Practitioner. b. Medically Necessary Treatment not available at location. c. Air Ambulance provider registered entity in India (except Global plans). d. Insured Person in India and treatment in India only (except Global plans). e. No return transportation covered. f. Hospitalization claim must be admissible under B-1.1 or Global sections.",
#                 "page": 15,
#                 "plans": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Secure Global Plus"],
#                 "not_available": ["Optima Lite"],
#                 "limit": "Up to 500,000"
#             },
#             {
#                 "section_id": "B.2.2",
#                 "title": "Daily Cash for Shared Room",
#                 "content": "The Company shall pay a daily cash amount as specified in Policy Schedule for each continuous and completed 24 hours of Hospitalization during the Policy Year if the Insured Person is Hospitalised in shared accommodation in a Network Provider Hospital and such Hospitalization exceeds 48 consecutive hours. Specific Conditions: a. Not available for time spent in ICU. b. Claim only payable if hospitalization claim admissible under B-1.1. Amount: 800 per day max upto 4800 (Optima Suraksha/Secure/Super/Global), 1000 per day max up to 6000 (Optima Select).",
#                 "page": 15,
#                 "plans": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select"],
#                 "not_available": ["Optima Lite", "Optima Secure Global Plus"],
#                 "geography": "India only"
#             },
#             {
#                 "section_id": "B.2.3",
#                 "title": "Protect Benefit",
#                 "content": "The Company shall indemnify the Insured Person for the Non-Medical Expenses listed under Annexure B to this Policy incurred in relation to a claim admissible under Section B-1 (Base Coverage) during the Policy Year. Exclusion (k) of Section C.2 - Specific Exclusions shall not apply to this Cover. In plans where Protect Benefit is available as optional cover, can be opted only at inception or renewals and once opted can be opted out at renewals.",
#                 "page": 15,
#                 "plans": ["Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Secure Global Plus"],
#                 "optional_for": ["Optima Secure", "Optima Super", "Optima Secure Global"],
#                 "inbuilt_for": ["Optima Select", "Optima Secure Global Plus"],
#                 "not_available": ["Optima Suraksha", "Optima Lite"]
#             },
#             {
#                 "section_id": "B.2.4",
#                 "title": "Plus Benefit",
#                 "content": "On Renewal without break, 50% of Base Sum Insured added to Sum Insured. Can accumulate up to 100% of Base Sum Insured. Applied annually on completion of each Policy Year. Irrespective of claims made. Utilizable only for B-1 and B-2.3 claims. Individual: added individually. Floater: added to all Family Members. If individual renewed as floater, lowest Plus Benefit carried forward. If floater split, apportioned proportionately. If Sum Insured reduced, Plus Benefit reduced proportionately. If increased, calculated on last completed Policy Year. For multi-year policies, credited post each Policy Year. New Insured Persons eligible per Renewal terms. Can be opted only at inception/renewals, opted out only at renewals. Upon opting, accrued CB carried forward and CB benefit ceases.",
#                 "page": 16,
#                 "plans": ["Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Secure Global Plus"],
#                 "optional_for": ["Optima Secure", "Optima Super", "Optima Secure Global"],
#                 "inbuilt_for": ["Optima Select", "Optima Secure Global Plus"],
#                 "not_available": ["Optima Suraksha", "Optima Lite"],
#                 "percentage": "50%",
#                 "max_accumulation": "100%"
#             },
#             {
#                 "section_id": "B.2.5",
#                 "title": "Secure Benefit",
#                 "content": "Additional amount as specified in Policy Schedule available as Sum Insured for all claims admissible under Section B (Base Coverage) and Section B-2.3 (Protect Benefit). Conditions: a. Applied only once during each Policy Year, unutilized amount not carried forward. b. Can be utilized for any number of claims during Policy Year. c. Applicable only after exhaustion of Base Sum Insured. d. Family floater: available on floater basis for all Insured Persons.",
#                 "page": 17,
#                 "plans": ["Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Secure Global Plus"],
#                 "not_available": ["Optima Suraksha", "Optima Lite"],
#                 "amount": "Equal to 100% of Base sum insured",
#                 "geography": "India only"
#             },
#             {
#                 "section_id": "B.2.6",
#                 "title": "Automatic Restore Benefit",
#                 "content": "Company instantly adds 100% of Base Sum Insured in event of admissible claim during Policy Year due to which Sum Insured was partially or completely exhausted. Conditions: i. Applied only once during Policy Year unless 'Unlimited Times' specified. ii. Restored amount only for subsequent claims during remainder of Policy Year. iii. Only for B-1 and B-2.3 claims. iv. Single claim never exceeds cumulative of: Base Sum Insured + CB + Plus Benefit + Secure Benefit. v. Restored Sum Insured usable by claimant and other Insured Persons. vi. Usable for same illness or other Illness. vii. Not carried forward if unutilized. viii. Family floater: available on floater basis.",
#                 "page": 17,
#                 "plans": ["Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Secure Global Plus"],
#                 "not_available": ["Optima Suraksha", "Optima Lite"],
#                 "restore_percentage": "100%",
#                 "trigger": "Unlimited times or once per policy year"
#             },
#             {
#                 "section_id": "B.2.7",
#                 "title": "Aggregate Deductible",
#                 "content": "Insured Person bears amount equal to Aggregate Deductible specified on Policy Schedule once in Policy Year post which coverage commences. Can be exhausted by providing invoices of one or more hospitalizations admissible as per terms. Conditions: a. Applicable on annual aggregate basis, opted at inception or Renewals. Can be increased at Renewal. b. Individual Policy: entire amount exhausted per Insured Person. c. Family floater: entire amount exhausted by any one or more Insured Persons. d. Not applicable to B-2.8 (E-Opinion), B-3 (Preventive Health Check Up), B-2.9/B-2.10 (Global Health Cover), B-2.11 (Overseas Travel Secure). e. Preventive Health Check-up not available if Aggregate Deductible of INR 5 Lakhs. f. Preventive Health Check-up, Secure Benefit, CB/Plus Benefit, Automatic Restore, Daily Cash, Unlimited Restore not available if Aggregate Deductible of INR 10 Lakhs or more.",
#                 "page": 18,
#                 "plans": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Secure Global Plus"],
#                 "optional": True,
#                 "options": ["10K", "25K", "50K", "1L", "2L", "3L", "5L", "10L", "20L", "25L"],
#                 "geography": "India only"
#             },
#             {
#                 "section_id": "B.2.7.1",
#                 "title": "Waiver of Aggregate Deductible",
#                 "content": "Option to reduce or waive aggregate deductible only once in lifetime at Renewal, subject to underwriting. Conditions: a. Age of eldest Insured Person < 50 years at purchase. b. After 5 continuous Policy Years and age < 61 at time of availing. c. Continuity benefits of waiting period accrued offered even after availing. d. Applies to all Insured Persons once selected. e. Premium charged as per modification. f. If reduced or waived, eligible for benefits applicable in forthcoming Policy Years.",
#                 "page": 19
#             },
#             {
#                 "section_id": "B.2.8",
#                 "title": "E-Opinion for Critical Illness",
#                 "content": "Company provides E-opinion facility for Critical Illness listed. E-opinion from Medical Practitioner within network. Specific Conditions: a. Subject to eligible geography of Network Provider. b. Individual policies: once per Policy Year. c. Family Floater/Multi-individual: once per Policy Year for each Insured Person. d. Insured Person's discretion to follow advice. Information shared with Network Providers. e. No impact on Sum Insured. Disclaimer: Company not liable for damages from Network Provider services. 51 Major Medical Illnesses covered including Cancer, Open Chest CABG, Kidney failure requiring dialysis, Myocardial Infarction, Major Organ/Bone Marrow Transplantation, Multiple Sclerosis, Permanent Paralysis, Stroke, etc.",
#                 "page": 19,
#                 "plans": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Secure Global Plus"],
#                 "not_available": ["Optima Lite"],
#                 "geography": "In India for most plans, Global for Optima Secure Global/Plus and Optima Super"
#             },
#             {
#                 "section_id": "B.2.9",
#                 "title": "Global Health Cover (Emergency Treatments Only)",
#                 "content": "Benefits extended for Emergency Medical Expenses diagnosed and incurred outside India: Hospitalization Expenses, AYUSH Treatment, Organ Donor Expenses, Emergency Air Ambulance, Protect Benefit, Plus Benefit, E Opinion for Critical Illness. Conditions: i. Maximum liability: Base Sum Insured and Plus Benefit. ii. Aggregate Deductible not applicable, but Per Claim Deductible of Rs. 10,000 applies. iii. Normally payable on Reimbursement, Cashless may be arranged case by case. iv. Treatment in registered Hospital per local laws. v. Exchange rate as per RBI on date of payment. vi. Treatment must commence within 45 days of trip start. vii. No separate Sum Insured, claim reduces opted plan Sum Insured. Specific Exclusions: Planned treatments, Pre/Post-hospitalization, non-Life threatening conditions, treatment if sole reason for journey, orthopedic diseases except fractures/dislocations, Oncological diseases, territorial restrictions by Government of India.",
#                 "page": 21,
#                 "plans": ["Optima Secure Global", "Optima Secure Global Plus"],
#                 "not_available": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Select", "Optima Lite"],
#                 "coverage_type": "Emergency only"
#             },
#             {
#                 "section_id": "B.2.10",
#                 "title": "Global Health Cover (Emergency & Planned Treatments)",
#                 "content": "Benefits for both planned and Emergency Medical Expenses outside India: Hospitalization Expenses, AYUSH Treatment, Pre-Hospitalization cover, Post-Hospitalization cover, Organ Donor Expenses, Emergency Air Ambulance, Protect Benefit, Plus Benefit, E Opinion for Critical Illness. Conditions i-vii same as B.2.9. Additional: viii. Pre/Post-hospitalization overseas only if hospitalization overseas and claim admissible. ix. Pre/Post-hospitalization from overseas hospitalization but incurred in India not payable. x. If Migration/Portability initiated, waiting periods apply afresh for planned hospitalization claims only, from date Global cover came into force. Forced migration by company excluded.",
#                 "page": 22,
#                 "plans": ["Optima Secure Global Plus"],
#                 "not_available": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Secure Global", "Optima Select", "Optima Lite"],
#                 "coverage_type": "Emergency and Planned"
#             },
#             {
#                 "section_id": "B.2.11",
#                 "title": "Overseas Travel Secure",
#                 "content": "Can only be opted with Optima Secure Global Plan or Optima Secure Global Plus Plan on additional premium. Payable up to Sum Insured only if: a. Overseas treating Medical Practitioner advised minimum 5 consecutive days hospitalization and requirement of accompanying person. b. Claim accepted under B.2.9 or B.2.10. No separate Sum Insured, claim reduces opted plan Sum Insured. Covers: 1. Travel Expenses - air tickets (most basic economy class) for Hospitalized Insured Person and one accompanying person. For Emergency: accompanying person two-way from City of Residence/India to nearest airport; Insured Person only from nearest airport to India. For planned: both two-way from India. If accompanying person already present, only return to India. 2. Accommodation Expenses - for accompanying person near hospitalization site, up to Rs. 15,000 per day for days Insured person hospitalized, maximum 30 days in Policy Year. Meals, laundry, transport not covered.",
#                 "page": 23,
#                 "plans": ["Optima Secure Global", "Optima Secure Global Plus"],
#                 "not_available": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Select", "Optima Lite"],
#                 "optional": True
#             },
#             {
#                 "section_id": "B.2.12",
#                 "title": "PED Waiting Period Modification",
#                 "content": "On availing, Pre-existing Disease Waiting Period modified as stipulated in Policy Schedule. Allowed at channel level only at policy inception, not by individual policyholders. Once selected cannot be opted out. Options: 1. Modification from 36 months to 24 months (2 years). 2. Modification from 36 months to 12 months (1 year).",
#                 "page": 25,
#                 "plans": ["All plans"],
#                 "channel_level_only": True,
#                 "options": ["24 months", "12 months"]
#             },
#             {
#                 "section_id": "B.2.13",
#                 "title": "Modification of Room Rent",
#                 "content": "Room Rent category modified as stipulated in Policy Schedule. Re-configurable at renewals subject to Underwriting. Options: 1. At Actuals to upto 1% of base sum insured per day AND ICU from At Actuals to upto 2% (Optima Lite inbuilt, not available other plans). 2. At Actuals to upto Single Private room (Optima Select inbuilt, not available other plans). 3. Single Private room to At Actuals (Optima Select customers only). 4. Single Private room to Shared room (Optima Select customers only, ICU remains At Actuals).",
#                 "page": 25,
#                 "plan_specific": True
#             },
#             {
#                 "section_id": "B.2.14",
#                 "title": "Modification of Pre-Hospitalization Expenses - Days",
#                 "content": "Pre-hospitalization medical expenses days modified as stipulated. Option: Modification from 60 days to 30 days. This is inbuilt in Optima Lite plan. Not available with any other plan.",
#                 "page": 26,
#                 "optima_lite_only": True,
#                 "standard_days": 60,
#                 "modified_days": 30
#             },
#             {
#                 "section_id": "B.2.15",
#                 "title": "Modification of Post-Hospitalization Expenses - Days",
#                 "content": "Post-hospitalization expenses days modified as stipulated. Option: Modification from 180 days to 60 days. This is inbuilt in Optima Lite plan. Not available with any other plan.",
#                 "page": 26,
#                 "optima_lite_only": True,
#                 "standard_days": 180,
#                 "modified_days": 60
#             },
#             {
#                 "section_id": "B.2.16",
#                 "title": "Modification of Cumulative Bonus",
#                 "content": "Percentage of cumulative bonus modified as stipulated. Option: Modification from 10% of Base Sum Insured upto 100% to 25% of Base Sum Insured upto 100%. This is inbuilt in Optima Select plan. Not available with any other plan.",
#                 "page": 27,
#                 "optima_select_only": True,
#                 "standard_percentage": "10%",
#                 "modified_percentage": "25%"
#             }
#         ]
        
#         for coverage in optional_coverages:
#             chunk = self.create_chunk(
#                 content=f"{coverage['section_id']}. {coverage['title']}: {coverage['content']}",
#                 metadata={
#                     "section": "B.2",
#                     "subsection": coverage['section_id'],
#                     "title": coverage['title'],
#                     "type": "optional_coverage",
#                     "page": coverage['page'],
#                     "plans": coverage.get('plans', []),
#                     "not_available": coverage.get('not_available', []),
#                     "optional": coverage.get('optional', False),
#                     "geography": coverage.get('geography', 'India')
#                 }
#             )
#             self.chunks.append(chunk)
    
#     def _chunk_renewal_benefits(self):
#         """Section B.3 - Renewal Benefits"""
        
#         renewal_benefits = [
#             {
#                 "section_id": "B.3",
#                 "title": "Preventive Health Check-up",
#                 "content": "On completion of each Policy Year where benefit was in force, Company indemnifies cost of Preventive Health Check-up for Insured Persons insured during previous Policy Year, up to specified amounts. Conditions: i. Available every Policy Year post first Policy Year completion, irrespective of policy tenure. Tests must be taken in eligible Policy Year. ii. Does NOT carry forward if not claimed. iii. Amount specified is maximum liability, does not reduce Sum Insured. iv. Applicable only if stipulated on Policy Schedule. v. Can be opted only at inception or renewals, opted out at renewals only. vi. Amount eligible as per Base Sum Insured of expiring Policy. Individual Policy limits: 5&7.5Lacs: Rs.1,500; 10Lacs: Rs.2,000; 15Lacs: Rs.4,000; 20,25,50&75Lakhs: Rs.5,000; 100&200Lacs: Rs.8,000. Family Floater limits: 5&7.5Lacs: Rs.2,500; 10Lacs: Rs.5,000; 15Lacs: Rs.8,000; 20,25,50&75Lakhs: Rs.10,000; 100&200Lacs: Rs.15,000. Not available if Aggregate Deductible of INR 5 Lakhs or more in force.",
#                 "page": 27,
#                 "optional_for": ["Optima Select"],
#                 "inbuilt_for": ["Optima Suraksha", "Optima Secure", "Optima Super", "Optima Secure Global", "Optima Lite", "Optima Secure Global Plus"]
#             }
#         ]
        
#         for benefit in renewal_benefits:
#             chunk = self.create_chunk(
#                 content=f"{benefit['section_id']}. {benefit['title']}: {benefit['content']}",
#                 metadata={
#                     "section": "B.3",
#                     "subsection": benefit['section_id'],
#                     "title": benefit['title'],
#                     "type": "renewal_benefit",
#                     "page": benefit['page'],
#                     "optional_for": benefit.get('optional_for', []),
#                     "inbuilt_for": benefit.get('inbuilt_for', [])
#                 }
#             )
#             self.chunks.append(chunk)
    
#     def _chunk_waiting_periods(self):
#         """Section C.1 - Waiting Periods"""
        
#         waiting_periods = [
#             {
#                 "code": "Excl01",
#                 "title": "Pre-Existing Diseases",
#                 "content": "Expenses related to treatment of pre-existing disease (PED) and its direct complications excluded until expiry of 36 months (unless specified otherwise in Policy Schedule) of continuous coverage after date of inception of first policy with insurer. In case of enhancement of Sum Insured, exclusion applies afresh to extent of increase. If continuously covered without break as per portability norms, waiting period reduced to extent of prior coverage. Coverage after 36 months subject to declaration at application and acceptance by Company.",
#                 "page": 28,
#                 "default_months": 36,
#                 "modifiable": True
#             },
#             {
#                 "code": "Excl02",
#                 "title": "Specified Disease/Procedure Waiting Period",
#                 "content": "Expenses related to treatment of listed Conditions, surgeries/treatments excluded until expiry of 24 months of continuous coverage after date of inception of first Policy. Not applicable for claims arising due to Accident. In case of enhancement of Sum Insured, exclusion applies afresh to extent of increase. If specified disease/procedure falls under PED waiting period, longer of two applies. Applies even if contracted after Policy or declared without specific loading. If continuously covered without break per IRDAI portability norms, waiting period reduced to extent of prior coverage. Listed Illnesses: Non infective Arthritis, Pilonidal sinus, Diseases of gall bladder including calculus diseases, Benign tumors/cysts/nodules/polyps including breast lumps, Urogenital system diseases (Kidney stone, Urinary Bladder Stone), Pancreatitis, Ulcer and erosion of stomach and duodenum, Polycystic ovarian diseases, All forms of Cirrhosis, GERD, Sinusitis/Rhinitis, Perineal/Perianal Abscesses, Skin tumors, Cataract and retina disorders, Gout/rheumatism, Tonsillitis, Osteoarthritis/osteoporosis, Fibroids, Benign Hyperplasia of Prostate. Surgical Procedures: Adenoidectomy/tonsillectomy, Tympanoplasty/Mastoidectomy, Hernia, D&C, Nasal concha resection, Surgery for prolapsed inter vertebral disc, Surgery for varicose veins/varicose ulcers, Myomectomy for fibroids, Surgery of Genito urinary system (unless malignancy), Surgery on prostate, Cholecystectomy, Surgery for Perianal Abscesses, Hydrocele/Rectocele, Joint replacement surgeries, Surgery for Nasal septum deviation, Ligament/Tendon/Meniscal tear, Hysterectomy, Fissurectomy/Haemorrhoidectomy/Fistulectomy/ENT surgeries, Endometriosis, Prolapsed Uterus, Rectal Prolapse, Varicocele, Retinal detachment, Glaucoma, Nasal polypectomy.",
#                 "page": 28,
#                 "months": 24,
#                 "exclusions": "Accident"
#             },
#             {
#                 "code": "Excl03",
#                 "title": "30-day Waiting Period",
#                 "content": "Expenses related to treatment of any illness within 30 days from first Policy commencement date excluded except claims arising due to Accident, provided covered. Not applicable if continuous coverage for more than twelve months. Applicable to enhanced Sum Insured in event of granting higher Sum Insured.",
#                 "page": 30,
#                 "days": 30,
#                 "exclusions": "Accident, continuous coverage > 12 months"
#             }
#         ]
        
#         for wp in waiting_periods:
#             chunk = self.create_chunk(
#                 content=f"Code {wp['code']} - {wp['title']}: {wp['content']}",
#                 metadata={
#                     "section": "C.1",
#                     "code": wp['code'],
#                     "title": wp['title'],
#                     "type": "waiting_period",
#                     "page": wp['page'],
#                     "duration": wp.get('months', wp.get('days')),
#                     "unit": "months" if 'months' in wp else "days"
#                 }
#             )
#             self.chunks.append(chunk)
    
#     def _chunk_standard_exclusions(self):
#         """Section C.2 - Standard Exclusions"""
        
#         exclusions = [
#             {"code": "Excl04", "title": "Investigation & Evaluation", "content": "Expenses related to any admission primarily for diagnostics and evaluation purposes only are excluded. Any diagnostic expenses not related or not incidental to current diagnosis and treatment are excluded.", "page": 30},
#             {"code": "Excl05", "title": "Rest Cure, rehabilitation and respite care", "content": "Expenses related to any admission primarily for enforced bed rest and not for receiving treatment. Includes: i. Custodial care at home or nursing facility for personal care (bathing, dressing, moving) by skilled or non-skilled persons. ii. Any services for terminally ill to address physical, social, emotional and spiritual needs.", "page": 30},
#             {"code": "Excl06", "title": "Obesity/Weight control", "content": "Expenses related to surgical treatment of obesity not fulfilling all conditions: i. Surgery upon advice of Doctor; ii. Supported by clinical protocols; iii. Member 18 years or older; iv. BMI >= 40 OR BMI >= 35 with severe comorbidities (obesity-related cardiomyopathy, coronary heart disease, severe sleep apnoea, uncontrolled type 2 diabetes) following failure of less invasive methods.", "page": 30},
#             {"code": "Excl07", "title": "Change-of-Gender treatments", "content": "Expenses related to any treatment, including surgical management, to change characteristics of the body to those of the opposite sex.", "page": 31},
#             {"code": "Excl08", "title": "Cosmetic or plastic Surgery", "content": "Expenses for cosmetic or plastic surgery or any treatment to change appearance unless for reconstruction following Accident, Burn(s) or Cancer or as part of Medically Necessary Treatment to remove direct and immediate health risk. Must be certified by attending Medical Practitioner.", "page": 31},
#             {"code": "Excl09", "title": "Hazardous or Adventure Sports", "content": "Expenses related to any treatment necessitated due to participation as professional in Hazardous or Adventure sports including para-jumping, rock climbing, mountaineering, rafting, motor racing, horse racing, scuba diving, hand gliding, sky diving, deep-sea diving.", "page": 31},
#             {"code": "Excl10", "title": "Breach of Law", "content": "Expenses for treatment directly arising from or consequent upon any Insured Person committing or attempting to commit a breach of law with criminal intent.", "page": 31},
#             {"code": "Excl11", "title": "Excluded Providers", "content": "Expenses incurred towards treatment in any hospital or by any Medical Practitioner or provider specifically excluded by Insurer and disclosed on website. However, in Life Threatening Situations or following Accident, expenses up to stage of stabilization are payable but not complete claim.", "page": 31},
#             {"code": "Excl12", "title": "Alcoholism, drug or substance abuse", "content": "Treatment for Alcoholism, drug or substance abuse or any addictive condition and consequences thereof.", "page": 31},
#             {"code": "Excl13", "title": "Health hydros, nature cure clinics, spas", "content": "Treatments received in health hydros, nature cure clinics, spas or similar establishments or private beds registered as nursing home attached to such establishments or where admission arranged wholly or partly for domestic reasons.", "page": 31},
#             {"code": "Excl14", "title": "Dietary supplements", "content": "Dietary supplements and substances purchasable without prescription, including Vitamins, minerals and organic substances unless prescribed by Medical Practitioner as part of Hospitalization claim or Day Care procedure.", "page": 31},
#             {"code": "Excl15", "title": "Refractive Error", "content": "Expenses related to treatment for correction of eye sight due to refractive error less than 7.5 dioptres.", "page": 31},
#             {"code": "Excl16", "title": "Unproven Treatments", "content": "Expenses related to any unproven treatment, services and supplies. Unproven treatments lack significant medical documentation to support effectiveness.", "page": 31},
#             {"code": "Excl17", "title": "Sterility and Infertility", "content": "Expenses related to sterility and infertility including: i. Any contraception, sterilization; ii. Assisted Reproduction services (IVF, ZIFT, GIFT, ICSI); iii. Gestational Surrogacy; iv. Reversal of sterilization.", "page": 31},
#             {"code": "Excl18", "title": "Maternity", "content": "i. Medical treatment expenses traceable to childbirth (including complicated deliveries and caesarean sections) except ectopic pregnancy; ii. Expenses towards miscarriage (unless due to Accident) and lawful medical termination of pregnancy.", "page": 32}
#         ]
        
#         for ex in exclusions:
#             chunk = self.create_chunk(
#                 content=f"Code {ex['code']} - {ex['title']}: {ex['content']}",
#                 metadata={
#                     "section": "C.2",
#                     "code": ex['code'],
#                     "title": ex['title'],
#                     "type": "standard_exclusion",
#                     "page": ex['page']
#                 }
#             )
#             self.chunks.append(chunk)
    
#     def _chunk_specific_exclusions(self):
#         """Section C.3 - Specific Exclusions"""
        
#         specific_exclusions = [
#             {"letter": "a", "content": "War or any act of war, invasion, act of foreign enemy, civil war, public defence, rebellion, revolution, insurrection, military or usurped acts, Nuclear, Chemical or Biological attack or weapons, radiation of any kind.", "page": 32},
#             {"letter": "b", "content": "Aggregate Deductible - Claims/claim amount falling within Aggregate Deductible limit if opted and in force, as specified in the Policy Schedule.", "page": 32},
#             {"letter": "c", "content": "Any Insured Person committing or attempting to commit intentional self-injury or attempted suicide or suicide.", "page": 32},
#             {"letter": "d", "content": "Any Insured Person's participation or involvement in naval, military or air force operation.", "page": 32},
#             {"letter": "e", "content": "Investigative treatment for sleep-apnoea, general debility or exhaustion ('run-down condition').", "page": 32},
#             {"letter": "f", "content": "Congenital external diseases, defects or anomalies.", "page": 32},
#             {"letter": "g", "content": "Stem cell harvesting.", "page": 32},
#             {"letter": "h", "content": "Investigative treatments for analysis and adjustments of spinal subluxation, diagnosis and treatment by manipulation of skeletal structure or for muscle stimulation except treatment of fractures (excluding hairline fractures) and dislocations of mandible and extremities.", "page": 32},
#             {"letter": "i", "content": "Circumcisions unless necessitated by Illness or Injury and forming part of treatment.", "page": 32},
#             {"letter": "j", "content": "Vaccination including inoculation and immunisations except post animal bite treatment.", "page": 32},
#             {"letter": "k", "content": "Non-Medical expenses such as food charges (other than patient's diet provided by hospital), laundry charges, attendant charges, ambulance collar, ambulance equipment, baby food, baby utility charges. Full list in ANNEXURE B at www.hdfcergo.com.", "page": 32},
#             {"letter": "l", "content": "Treatment taken on outpatient basis.", "page": 32},
#             {"letter": "m", "content": "The provision or fitting of hearing aids, spectacles or contact lenses.", "page": 32},
#             {"letter": "n", "content": "Any treatment and associated expenses for alopecia, baldness including cortico steroids and topical immuno therapy wigs, toupees, hair pieces, any non-surgical hair replacement methods, optometric services.", "page": 32},
#             {"letter": "o", "content": "Expenses for Artificial limbs and/or device used for diagnosis or treatment (except when used intra-operatively), prosthesis, corrective devices external durable medical equipment, wheelchairs, crutches, oxygen concentrator for bronchial asthma/COPD, cost of cochlear implant(s) unless necessitated by Accident.", "page": 33},
#             {"letter": "p", "content": "Any treatment or part of treatment not of reasonable charge and not Medically Necessary. Drugs or treatments not supported by prescription.", "page": 33},
#             {"letter": "q", "content": "Any permanent exclusion applied on medical or physical condition or treatment as specifically mentioned in Policy Schedule and accepted by Policyholder/Insured Person. Such exclusions applied for conditions/treatments that otherwise would have resulted in rejection of coverage as per Company's Underwriting Policy.", "page": 33}
#         ]
        
#         for ex in specific_exclusions:
#             chunk = self.create_chunk(
#                 content=f"Specific Exclusion {ex['letter']}: {ex['content']}",
#                 metadata={
#                     "section": "C.3",
#                     "exclusion_letter": ex['letter'],
#                     "type": "specific_exclusion",
#                     "page": ex['page']
#                 }
#             )
#             self.chunks.append(chunk)
    
#     def _chunk_general_terms(self):
#         """Sections D.1 and E - General Terms and Clauses"""
        
#         general_terms = [
#             {
#                 "section_id": "D.1.1",
#                 "title": "Disclosure of Information",
#                 "content": "Policy shall be void and all premium paid forfeited to Company in event of misrepresentation, mis-description or non-disclosure of any material fact by Policyholder.",
#                 "page": 33
#             },
#             {
#                 "section_id": "D.1.2",
#                 "title": "Condition Precedent to Admission of Liability",
#                 "content": "Terms and conditions of policy must be fulfilled by insured person for Company to make any payment for claim(s).",
#                 "page": 33
#             },
#             {
#                 "section_id": "D.1.3",
#                 "title": "Claim Settlement (Penal Interest)",
#                 "content": "Company shall settle or reject claim within 15 days from date of receipt of intimation. In case of delay in payment, Company liable to pay interest at rate 2% above bank rate from date of receipt of intimation to date of payment.",
#                 "page": 33
#             },
#             {
#                 "section_id": "D.1.6",
#                 "title": "Moratorium Period",
#                 "content": "After 60 continuous months of coverage (including portability and migration), no policy and claim contestable by insurer on grounds of non-disclosure, misrepresentation, except on grounds of established fraud. Applicable for sums insured of first policy. For enhanced sum insured, 60 months applicable from date of enhancement on enhanced limits only.",
#                 "page": 34
#             },
#             {
#                 "section_id": "D.1.7",
#                 "title": "Fraud",
#                 "content": "If claim fraudulent, or false statement/declaration made, or fraudulent means used to obtain benefit, all benefits and premium forfeited. Any amount paid against fraudulent claims to be repaid. Fraud means: suggesting as fact what is not true and not believed true; active concealment of fact; any act fitted to deceive; any act/omission law specially declares to be fraudulent. Company shall not repudiate on ground of Fraud if mis-statement true to best of knowledge and no deliberate intention to suppress.",
#                 "page": 34
#             },
#             {
#                 "section_id": "D.1.8",
#                 "title": "Free look Period",
#                 "content": "Applicable on new individual policies, not renewals or porting/migrating. 30 days from date of receipt of policy document to review and return. If no claim during Free Look Period: refund of premium less medical examination expenses and stamp duty; or proportionate risk premium if risk commenced; or proportionate premium commensurate with coverage if partial coverage commenced.",
#                 "page": 35
#             },
#             {
#                 "section_id": "D.1.9",
#                 "title": "Renewal of Policy",
#                 "content": "Policy renewable except on grounds of established fraud or non-disclosure/misrepresentation, provided not withdrawn and subject to Moratorium clause. a) Not denied on ground of claims in preceding years (except benefit-based policies). b) Delay condoned up to grace period without break. c) No loading on renewals based on individual claims experience. d) No fresh underwriting unless increase in sum insured; may underwrite only increased amount. e) Renewal premium payable prior to due date as per norms.",
#                 "page": 35
#             },
#             {
#                 "section_id": "D.1.10",
#                 "title": "Portability",
#                 "content": "Option to port Policy to other insurers by applying at least 30 days before, but not earlier than 60 days from policy renewal date per IRDAI guidelines. If continuously covered without lapses under any health insurance policy with Indian General/Health insurer, accrued continuity benefits in waiting periods as per IRDAI guidelines.",
#                 "page": 36
#             },
#             {
#                 "section_id": "D.1.11",
#                 "title": "Migration",
#                 "content": "Option to migrate Policy to other products/plans offered by Company by applying at least 30 days before renewal date per IRDAI guidelines. If continuously covered without lapses under any Company product/plan, accrued continuity benefits in waiting periods as per IRDAI guidelines.",
#                 "page": 36
#             },
#             {
#                 "section_id": "D.1.18",
#                 "title": "Non-Disclosure or Misrepresentation of Pre-Existing Disease",
#                 "content": "Company may exercise options for continuing coverage in case of non-disclosure/misrepresentation of PED, subject to prior consent: a. Permanently exclude disease/condition and continue. b. Incorporate additional Waiting Period not exceeding 3 years from date non-disclosed condition detected. c. Levy underwriting loading from first Policy Year or Renewal.",
#                 "page": 39
#             },
#             {
#                 "section_id": "D.1.19",
#                 "title": "Utilization of Sum Insured",
#                 "content": "Sequence of utilization: a. Aggregate Deductible; b. Base Sum Insured; c. Cumulative Bonus/Plus Benefit; d. Secure Benefit; e. Automatic Restore Benefit. Single claim never exceeds cumulative of: Base Sum Insured + CB + Plus Benefit + Secure Benefit.",
#                 "page": 39
#             },
#             {
#                 "section_id": "D.1.20",
#                 "title": "Geography",
#                 "content": "Coverage throughout territory of India, except under Section B-2.8 (E-Opinion), B-2.9 Global Health Cover (Emergency), B-2.10 Global Health Cover (Emergency & Planned), B-2.11 Overseas Travel Secure and as specified in Schedule of Coverage.",
#                 "page": 40
#             },
#             {
#                 "section_id": "E.1.1",
#                 "title": "Notification of Claim",
#                 "content": "Notice with full particulars: a. Within 24 hours from date of emergency Hospitalization or before discharge, whichever earlier. b. At least 48 hours prior to admission for planned Hospitalization or decision to avail Home Health Care.",
#                 "page": 41
#             },
#             {
#                 "section_id": "E.1.2",
#                 "title": "Cashless Claims Procedure in India",
#                 "content": "Treatment in Network Provider subject to pre-authorization. Cashless request form available with Network Provider. Network Provider obtains information and sends request to Company. Company issues pre-authorization letter after assessment. At discharge, Insured Person verifies and signs discharge papers, pays non-medical and inadmissible expenses. Company reserves right to deny pre-authorization if unable to provide relevant medical details. If cashless denied, may obtain treatment and submit for reimbursement.",
#                 "page": 41
#             },
#             {
#                 "section_id": "E.1.6",
#                 "title": "Reimbursement Claims Time Limits",
#                 "content": "Hospitalization, Day Care, Pre-Hospitalization: Within 30 days of discharge. Post-Hospitalization: Within 15 days from completion of post-Hospitalization treatment.",
#                 "page": 43
#             }
#         ]
        
#         for term in general_terms:
#             chunk = self.create_chunk(
#                 content=f"{term['section_id']}. {term['title']}: {term['content']}",
#                 metadata={
#                     "section": term['section_id'].split('.')[0],
#                     "subsection": term['section_id'],
#                     "title": term['title'],
#                     "type": "general_term",
#                     "page": term['page']
#                 }
#             )
#             self.chunks.append(chunk)
    
#     def _chunk_annexures(self):
#         """Annexure A, B, C"""
        
#         # Annexure A - Insurance Ombudsman (simplified, key info)
#         chunk_a = self.create_chunk(
#             content="Annexure A: Contact details of Offices of Insurance Ombudsman. Key offices: AHMEDABAD (Gujarat, Dadra & Nagar Haveli, Daman and Diu), BENGALURU (Karnataka), BHOPAL (Madhya Pradesh, Chhattisgarh), BHUBANESWAR (Odisha), CHANDIGARH (Punjab, Haryana excluding Gurugram/Faridabad/Sonepat/Bahadurgarh, Himachal Pradesh, J&K, Ladakh, Chandigarh), CHENNAI (Tamil Nadu, Puducherry), DELHI (Delhi, Gurugram, Faridabad, Sonepat, Bahadurgarh), GUWAHATI (North East states), HYDERABAD (Andhra Pradesh, Telangana, Yanam), JAIPUR (Rajasthan), KOCHI (Kerala, Lakshadweep, Mahe), KOLKATA (West Bengal, Sikkim, Andaman & Nicobar), LUCKNOW (Uttar Pradesh districts), MUMBAI (Mumbai Metropolitan Region), NOIDA (Uttarakhand, UP districts), PATNA (Bihar, Jharkhand), PUNE (Goa, Maharashtra excluding Navi Mumbai/Thane/Palghar/Raigad/Mumbai), THANE (Navi Mumbai, Thane, Palghar, Raigad, Mumbai wards M/E, M/W, N, S, T).",
#             metadata={
#                 "section": "Annexure A",
#                 "type": "ombudsman_contacts",
#                 "page": 46
#             }
#         )
#         self.chunks.append(chunk_a)
        
#         # Annexure B - Non-Medical Expenses (key categories)
#         chunk_b = self.create_chunk(
#             content="Annexure B: Items for which Coverage not available (Non-Medical Expenses). Categories: Baby items (food, utilities), Personal services (beauty, laundry, telephone, email/internet, guest services), Medical accessories (belts, braces, cold/hot packs, carry bags, leggings, crepe bandage, diapers, eyelet collar, slings), Equipment (oxygen cylinder outside hospital, spacer, spirometre, nebulizer kit, steam inhaler, arm sling, thermometer, cervical collar, splint, nimbus/water/air bed, ambulance collar/equipment, abdominal binder), Nursing (private nurses, special nursing), Consumables (sugar free tablets, ECG electrodes, gloves, nebulisation kit, kits without details, kidney tray, mask, ounce glass, oxygen mask, pelvic traction belt, pan can, trolley cover, urometer/urine jug, vasofix safety), Documentation (birth certificate, certificate charges, courier, conveyance, medical certificate, records, photocopies), Other (food other than patient diet, extra diet, mortuary charges, walking aids, service charges where nursing also charged, television, surcharges, attendant charges).",
#             metadata={
#                 "section": "Annexure B",
#                 "type": "non_medical_exclusions",
#                 "page": 49
#             }
#         )
#         self.chunks.append(chunk_b)
        
#         # Annexure C - Plan Comparison (broken into plan-specific chunks)
#         plans = [
#             {
#                 "name": "Optima Suraksha",
#                 "details": "Base Sum Insured: 5/10/15/20/25/50 Lakhs. Geography: India only. Room Rent: At Actuals. ICU: At Actuals. Pre-Hospitalization: 60 days. Post-Hospitalization: 180 days. Cumulative Bonus: Not Covered. Emergency Air Ambulance: Covered Up to 500,000. Daily Cash Shared Room: 800/day max 4800. Protect Benefit: Not Covered. Plus Benefit: Not Covered. Secure Benefit: Not Covered. Automatic Restore: Equal to 100% of Base sum insured. Aggregate Deductible: Optional 10K-10L. E-Opinion: In India. Global Cover: Not Covered. Preventive Health Check-up: Inbuilt.",
#                 "page": 50
#             },
#             {
#                 "name": "Optima Secure",
#                 "details": "Base Sum Insured: 5/10/15/20/25/50/100/200 Lakhs. Geography: India only. Room Rent: At Actuals. ICU: At Actuals. Pre-Hospitalization: 60 days. Post-Hospitalization: 180 days. Cumulative Bonus: Not Covered. Emergency Air Ambulance: Covered Up to 500,000. Daily Cash Shared Room: 800/day max 4800. Protect Benefit: Covered up to sum insured. Plus Benefit: Optional (50% of Base SI, max 100%). Secure Benefit: Equal to 100% of Base sum insured. Automatic Restore: Unlimited times. Aggregate Deductible: Optional 10K-25L. E-Opinion: In India. Global Cover: Not Covered. Preventive Health Check-up: Inbuilt.",
#                 "page": 50
#             },
#             {
#                 "name": "Optima Super",
#                 "details": "Base Sum Insured: 5/7.5/10/15/20/25/50/100/200 Lakhs. Geography: India only. Room Rent: At Actuals. ICU: At Actuals. Pre-Hospitalization: 60 days. Post-Hospitalization: 180 days. Cumulative Bonus: Not Covered. Emergency Air Ambulance: Covered Up to 500,000. Daily Cash Shared Room: 800/day max 4800. Protect Benefit: Covered up to sum insured. Plus Benefit: Optional (50% of Base SI, max 100%). Secure Benefit: Equal to 200% of Base sum insured. Automatic Restore: Unlimited times. Aggregate Deductible: Optional 10K-25L. E-Opinion: Global. Global Cover: Not Covered. Preventive Health Check-up: Inbuilt.",
#                 "page": 50
#             },
#             {
#                 "name": "Optima Secure Global",
#                 "details": "Base Sum Insured: All figures in 25/50/75/100/200 Lakhs. Geography: Worldwide including India. Room Rent: At Actuals. ICU: At Actuals. Pre-Hospitalization: 60 days (India only). Post-Hospitalization: 180 days (India only). Cumulative Bonus: Not Covered. Emergency Air Ambulance: Covered Up to 500,000. Daily Cash Shared Room: 800/day max 4800 (India only). Protect Benefit: Covered up to sum insured. Plus Benefit: Optional (50% of Base SI, max 100%). Secure Benefit: Equal to 100% of Base sum insured (India only). Automatic Restore: Unlimited times (India only). Aggregate Deductible: Optional 10K-25L (India only). E-Opinion: Global. Global Cover: Emergency Treatments Only (Outside India only). Overseas Travel Secure: Optional. Preventive Health Check-up: Inbuilt.",
#                 "page": 50
#             },
#             {
#                 "name": "Optima Select",
#                 "details": "Base Sum Insured: 5/10/15/20/25/50/100/200 Lakhs. Geography: India only. Room Rent: Upto Single Private room (or At Actuals/Shared room if modified). ICU: At Actuals. Pre-Hospitalization: 60 days. Post-Hospitalization: 180 days. Cumulative Bonus: 25% of Base SI max 100%. Emergency Air Ambulance: Covered Up to 500,000. Daily Cash Shared Room: 1000/day max 6000. Protect Benefit: Covered up to sum insured. Plus Benefit: Inbuilt (50% of Base SI, max 100%). Secure Benefit: Equal to 100% of Base sum insured. Automatic Restore: Unlimited times. Aggregate Deductible: Optional 10K-25L. E-Opinion: Global. Global Cover: Not Covered. PED modification: Optional. Room Rent modification: Optional (At Actuals or Shared). Preventive Health Check-up: Optional.",
#                 "page": 50
#             },
#             {
#                 "name": "Optima Lite",
#                 "details": "Base Sum Insured: 5/7.5 Lakhs. Geography: India only. Room Rent: Upto 1% of base sum insured per day. ICU: Upto 2% of base sum insured per day. Pre-Hospitalization: 30 days. Post-Hospitalization: 60 days. Cumulative Bonus: 10% of Base SI max 100%. Emergency Air Ambulance: Covered Up to 500,000. Daily Cash Shared Room: Not Covered. Protect Benefit: Not Covered. Plus Benefit: Optional (50% of Base SI, max 100%). Secure Benefit: Not Covered. Automatic Restore: Equal to 100% of Base sum insured. Aggregate Deductible: Optional 10K-10L. E-Opinion: Not Covered. Global Cover: Not Covered. Preventive Health Check-up: Inbuilt.",
#                 "page": 50
#             },
#             {
#                 "name": "Optima Secure Global Plus",
#                 "details": "Base Sum Insured: 25/50/75/100/200 Lakhs. Geography: Worldwide including India. Room Rent: At Actuals. ICU: At Actuals. Pre-Hospitalization: 60 days (India only). Post-Hospitalization: 180 days (India only). Cumulative Bonus: Not Covered. Emergency Air Ambulance: Covered Up to 500,000. Daily Cash Shared Room: Not Covered. Protect Benefit: Covered up to sum insured. Plus Benefit: Inbuilt (50% of Base SI, max 100%). Secure Benefit: Equal to 100% of Base sum insured (India only). Automatic Restore: Unlimited times (India only). Aggregate Deductible: Optional 10K-25L (India only). E-Opinion: Global. Global Cover: Emergency and Planned Treatments (Outside India only). Overseas Travel Secure: Optional. Preventive Health Check-up: Inbuilt.",
#                 "page": 50
#             }
#         ]
        
#         for plan in plans:
#             chunk = self.create_chunk(
#                 content=f"Annexure C - {plan['name']} Plan: {plan['details']}",
#                 metadata={
#                     "section": "Annexure C",
#                     "type": "plan_comparison",
#                     "plan_name": plan['name'],
#                     "page": plan['page']
#                 }
#             )
#             self.chunks.append(chunk)


# # ============ USAGE ============

# def main():
#     """Generate chunks and save to JSON"""
#     chunker = PolicyDocumentChunker()
#     chunks = chunker.chunk_document()
    
#     # Save to JSON file
#     output_file = "hdfc_ergo_policy_chunks.json"
#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(chunks, f, indent=2, ensure_ascii=False)
    
#     print(f"Generated {len(chunks)} chunks")
#     print(f"Saved to: {output_file}")
    
#     # Print sample chunks
#     print("\n" + "="*80)
#     print("SAMPLE CHUNKS:")
#     print("="*80)
    
#     samples = [0, 35, 78, 95, 110]  # Different section samples
#     for idx in samples:
#         if idx < len(chunks):
#             chunk = chunks[idx]
#             print(f"\n--- Chunk {idx+1}/{len(chunks)} | ID: {chunk['id']} ---")
#             print(f"Section: {chunk['metadata']['section']}")
#             print(f"Type: {chunk['metadata']['type']}")
#             print(f"Content (first 300 chars): {chunk['content'][:300]}...")
    
#     return chunks

# if __name__ == "__main__":
#     chunks = main()




"""
Policy Document Chunker for HDFC ERGO Insurance Documents

Preserves ALL content including contact information and tables.
Tables are converted to Markdown format for structure preservation.
"""

import json
import re
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

# PDF processing
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    print("Warning: pdfplumber not installed. Install with: pip install pdfplumber")


@dataclass
class Chunk:
    """Represents a single chunk of the document with metadata."""
    id: str
    content: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        """Convert chunk to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata
        }


class PolicyDocumentChunker:
    """
    Main chunker class for insurance policy documents.
    Preserves all content including contact information and tables.
    """
    
    def __init__(self, pdf_path: Optional[str] = None):
        self.pdf_path = pdf_path
        self.chunks: List[Chunk] = []
        self.chunk_counter = 0
        
        # Patterns for detecting section types
        self._compile_section_patterns()
    
    def _compile_section_patterns(self):
        """Compile patterns for detecting section types from headers."""
        
        # Map patterns to (section_code, section_name, content_type)
        self.section_patterns = [
            # Definitions
            (r'section\s+a\.?1\.?1|standard\s+definitions', 'A.1.1', 'Standard Definitions', 'definitions'),
            (r'section\s+a\.?1\.?2|specific\s+definitions', 'A.1.2', 'Specific Definitions', 'definitions'),
            
            # Benefits
            (r'section\s+b\.?1\.?1\.?1|other\s+expenses', 'B.1.1.1', 'Other Expenses - Hospitalization', 'base_coverage'),
            (r'section\s+b\.?1\.?1|hospitalization\s+expenses', 'B.1.1', 'Hospitalization Expenses', 'base_coverage'),
            (r'section\s+b\.?1\.?2|home\s+health\s+care', 'B.1.2', 'Home Health Care', 'base_coverage'),
            (r'section\s+b\.?1\.?3|domiciliary', 'B.1.3', 'Domiciliary Hospitalization', 'base_coverage'),
            (r'section\s+b\.?1\.?4|ayush\s+treatment', 'B.1.4', 'AYUSH Treatment', 'base_coverage'),
            (r'section\s+b\.?1\.?5|pre-hospitalization', 'B.1.5', 'Pre-Hospitalization Expenses', 'base_coverage'),
            (r'section\s+b\.?1\.?6|post-hospitalization', 'B.1.6', 'Post-Hospitalization Expenses', 'base_coverage'),
            (r'section\s+b\.?1\.?7|organ\s+donor', 'B.1.7', 'Organ Donor Expenses', 'base_coverage'),
            (r'section\s+b\.?1\.?8|cumulative\s+bonus', 'B.1.8', 'Cumulative Bonus', 'base_coverage'),
            
            # Optional Coverages
            (r'section\s+b\.?2\.?1|emergency\s+air\s+ambulance', 'B.2.1', 'Emergency Air Ambulance', 'optional_coverage'),
            (r'section\s+b\.?2\.?2|daily\s+cash', 'B.2.2', 'Daily Cash for Shared Room', 'optional_coverage'),
            (r'section\s+b\.?2\.?3|protect\s+benefit', 'B.2.3', 'Protect Benefit', 'optional_coverage'),
            (r'section\s+b\.?2\.?4|plus\s+benefit', 'B.2.4', 'Plus Benefit', 'optional_coverage'),
            (r'section\s+b\.?2\.?5|secure\s+benefit', 'B.2.5', 'Secure Benefit', 'optional_coverage'),
            (r'section\s+b\.?2\.?6|automatic\s+restore', 'B.2.6', 'Automatic Restore Benefit', 'optional_coverage'),
            (r'section\s+b\.?2\.?7\.?1|waiver.*aggregate', 'B.2.7.1', 'Waiver of Aggregate Deductible', 'optional_coverage'),
            (r'section\s+b\.?2\.?7|aggregate\s+deductible', 'B.2.7', 'Aggregate Deductible', 'optional_coverage'),
            (r'section\s+b\.?2\.?8|e-opinion|critical\s+illness', 'B.2.8', 'E-Opinion for Critical Illness', 'optional_coverage'),
            (r'section\s+b\.?2\.?9|global\s+health.*emergency\s+only', 'B.2.9', 'Global Health Cover (Emergency)', 'optional_coverage'),
            (r'section\s+b\.?2\.?10|global\s+health.*planned', 'B.2.10', 'Global Health Cover (Emergency & Planned)', 'optional_coverage'),
            (r'section\s+b\.?2\.?11|overseas\s+travel', 'B.2.11', 'Overseas Travel Secure', 'optional_coverage'),
            (r'section\s+b\.?2\.?12|ped\s+waiting', 'B.2.12', 'PED Waiting Period Modification', 'optional_coverage'),
            (r'section\s+b\.?2\.?13|modification.*room\s+rent', 'B.2.13', 'Modification of Room Rent', 'optional_coverage'),
            (r'section\s+b\.?2\.?14|modification.*pre-hospitalization', 'B.2.14', 'Modification of Pre-Hospitalization', 'optional_coverage'),
            (r'section\s+b\.?2\.?15|modification.*post-hospitalization', 'B.2.15', 'Modification of Post-Hospitalization', 'optional_coverage'),
            (r'section\s+b\.?2\.?16|modification.*cumulative', 'B.2.16', 'Modification of Cumulative Bonus', 'optional_coverage'),
            
            # Renewal Benefits
            (r'section\s+b\.?3|renewal\s+benefit|preventive\s+health', 'B.3', 'Preventive Health Check-up', 'renewal_benefit'),
            
            # Waiting Periods & Exclusions
            (r'section\s+c\.?1|waiting\s+periods?', 'C.1', 'Waiting Periods', 'waiting_period'),
            (r'code\s+excl01|pre-existing\s+disease', 'C.1', 'Pre-Existing Diseases', 'waiting_period'),
            (r'code\s+excl02|specified\s+disease', 'C.1', 'Specified Disease/Procedure', 'waiting_period'),
            (r'code\s+excl03|30-day\s+waiting', 'C.1', '30-day Waiting Period', 'waiting_period'),
            (r'section\s+c\.?2|standard\s+exclusions?', 'C.2', 'Standard Exclusions', 'exclusion'),
            (r'code\s+excl\d+|investigation|obesity|cosmetic', 'C.2', 'Standard Exclusions', 'exclusion'),
            (r'section\s+c\.?3|specific\s+exclusions?', 'C.3', 'Specific Exclusions', 'exclusion'),
            
            # General Terms
            (r'section\s+d\.?1\.?1|disclosure', 'D.1.1', 'Disclosure of Information', 'general_term'),
            (r'section\s+d\.?1\.?2|condition\s+precedent', 'D.1.2', 'Condition Precedent', 'general_term'),
            (r'section\s+d\.?1\.?3|claim\s+settlement', 'D.1.3', 'Claim Settlement', 'general_term'),
            (r'section\s+d\.?1\.?6|moratorium', 'D.1.6', 'Moratorium Period', 'general_term'),
            (r'section\s+d\.?1\.?7|fraud', 'D.1.7', 'Fraud', 'general_term'),
            (r'section\s+d\.?1\.?8|free\s+look', 'D.1.8', 'Free Look Period', 'general_term'),
            (r'section\s+d\.?1\.?9|renewal', 'D.1.9', 'Renewal of Policy', 'general_term'),
            (r'section\s+d\.?1\.?10|portability', 'D.1.10', 'Portability', 'general_term'),
            (r'section\s+d\.?1\.?11|migration', 'D.1.11', 'Migration', 'general_term'),
            (r'section\s+d\.?1\.?18|non-disclosure.*ped', 'D.1.18', 'Non-Disclosure of PED', 'general_term'),
            (r'section\s+d\.?1\.?19|utilization.*sum\s+insured', 'D.1.19', 'Utilization of Sum Insured', 'general_term'),
            (r'section\s+d\.?1\.?20|geography', 'D.1.20', 'Geography', 'general_term'),
            
            # Claims
            (r'section\s+e\.?1\.?1|notification\s+of\s+claim', 'E.1.1', 'Notification of Claim', 'general_term'),
            (r'section\s+e\.?1\.?2|cashless.*india', 'E.1.2', 'Cashless Claims in India', 'general_term'),
            (r'section\s+e\.?1\.?6|reimbursement.*time', 'E.1.6', 'Reimbursement Claims Time Limits', 'general_term'),
            
            # Annexures - ALL preserved including contact info
            (r'annexure\s+a|ombudsman|contact\s+details.*offices?', 'Annexure_A', 'Contact Details of Insurance Ombudsman', 'ombudsman_contacts'),
            (r'annexure\s+b|non-medical\s+expenses', 'Annexure_B', 'Non-Medical Expenses', 'non_medical_exclusions'),
            (r'annexure\s+c|plan\s+chart|schedule\s+of\s+benefits', 'Annexure_C', 'Plan Comparison Chart', 'plan_comparison'),
        ]
        
        # Compile patterns
        self.compiled_section_patterns = [
            (re.compile(pattern, re.IGNORECASE), section_code, section_name, content_type)
            for pattern, section_code, section_name, content_type in self.section_patterns
        ]
    
    def _generate_id(self, prefix: str) -> str:
        """Generate unique chunk ID."""
        self.chunk_counter += 1
        clean_prefix = prefix.replace('.', '_').replace(' ', '_').replace('-', '_')[:25]
        hash_suffix = hashlib.md5(str(self.chunk_counter).encode()).hexdigest()[:6]
        return f"{clean_prefix}_{self.chunk_counter:03d}_{hash_suffix}"
    
    def _detect_section(self, text: str, page_num: int, default_section: str = "MISC") -> Tuple[str, str, str]:
        """
        Detect section type from text content.
        Returns (section_code, section_name, content_type)
        """
        text_sample = text[:800].lower() if text else ""
        
        for pattern, section_code, section_name, content_type in self.compiled_section_patterns:
            if pattern.search(text_sample):
                return (section_code, section_name, content_type)
        
        # Fallback based on page number
        if page_num <= 10:
            return ('A', 'Definitions', 'definitions')
        elif page_num <= 13:
            return ('B.1', 'Base Coverages', 'base_coverage')
        elif page_num <= 27:
            return ('B.2', 'Optional Coverages', 'optional_coverage')
        elif page_num == 27:
            return ('B.3', 'Renewal Benefits', 'renewal_benefit')
        elif page_num <= 30:
            return ('C.1', 'Waiting Periods', 'waiting_period')
        elif page_num <= 32:
            return ('C.2', 'Exclusions', 'exclusion')
        elif page_num <= 40:
            return ('D', 'General Terms', 'general_term')
        elif page_num <= 45:
            return ('E', 'Claims Procedure', 'general_term')
        else:
            return (default_section, 'Miscellaneous', 'miscellaneous')
    
    def _clean_header_footer(self, text: str) -> str:
        """Remove repetitive headers and footers while preserving content."""
        if not text:
            return ""
        
        # Patterns to remove (company branding, page numbers, legal text)
        removal_patterns = [
            r'HDFC ERGO General Insurance Company Limited\.?',
            r'Policy Wording my:Optima Secure',
            r'IRDAI Reg\.No\.146CIN:U66030MH2007PLC177117',
            r'Registered & Corporate Office:[^\n]*',
            r'UIN:my:Optima Secure -HDFHLIP25041V062425',
            r'^\s*\d+\s*$',  # Standalone page numbers
            r'www\.hdfcergo\.com',
        ]
        
        cleaned = text
        for pattern in removal_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE | re.MULTILINE)
        
        # Clean up excessive whitespace but preserve structure
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)  # Max 2 newlines
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)     # Normalize horizontal spaces
        
        return cleaned.strip()
    
    def _format_table_to_markdown(self, table_data: List[List[Any]]) -> Optional[str]:
        """
        Convert table data to Markdown format.
        Preserves ALL content including phone numbers, emails, addresses.
        """
        if not table_data or len(table_data) < 1:
            return None
        
        # Clean and normalize cells
        cleaned_rows = []
        for row in table_data:
            cleaned_cells = []
            for cell in row:
                if cell is None:
                    cell = ""
                cell_str = str(cell).strip()
                # Clean internal whitespace but preserve content
                cell_str = ' '.join(cell_str.split())
                cleaned_cells.append(cell_str)
            cleaned_rows.append(cleaned_cells)
        
        if not cleaned_rows:
            return None
        
        # Determine column count (handle ragged tables)
        max_cols = max(len(row) for row in cleaned_rows)
        
        # Normalize all rows to same column count
        normalized_rows = []
        for row in cleaned_rows:
            if len(row) < max_cols:
                row = row + [''] * (max_cols - len(row))
            normalized_rows.append(row[:max_cols])
        
        # Check if this is actually a data table (not just layout)
        non_empty_cells = sum(1 for row in normalized_rows for cell in row if cell)
        total_cells = len(normalized_rows) * max_cols
        if non_empty_cells / total_cells < 0.2:  # Less than 20% filled
            return None
        
        # Build markdown table
        lines = []
        
        # Header row
        header = '| ' + ' | '.join(normalized_rows[0]) + ' |'
        lines.append(header)
        
        # Separator
        separator = '|' + '|'.join(['---' for _ in range(max_cols)]) + '|'
        lines.append(separator)
        
        # Data rows
        for row in normalized_rows[1:]:
            # Keep row even if partially empty (for contact tables)
            row_str = '| ' + ' | '.join(row) + ' |'
            lines.append(row_str)
        
        return '\n'.join(lines)
    
    def _extract_table_metadata(self, table_data: List[List[Any]], page_num: int) -> Dict:
        """Extract metadata from table for better retrieval."""
        metadata = {
            "page": page_num,
            "content_type": "table",
            "row_count": len(table_data),
            "col_count": max(len(row) for row in table_data) if table_data else 0,
        }
        
        # Detect table type from content
        if not table_data:
            return metadata
        
        # Combine header and first few rows for analysis
        sample_text = ' '.join(
            str(cell).lower() for row in table_data[:3] for cell in row if cell
        )
        
        # Detect table type
        if 'ombudsman' in sample_text or 'jurisdiction' in sample_text:
            metadata['table_type'] = 'ombudsman_contacts'
            metadata['has_contact_info'] = True
        elif 'plan' in sample_text and ('optima' in sample_text or 'suraksha' in sample_text or 'secure' in sample_text):
            metadata['table_type'] = 'plan_comparison'
        elif 'item' in sample_text or 's. no.' in sample_text or 'non-medical' in sample_text:
            metadata['table_type'] = 'item_list'
        elif 'tel' in sample_text or 'email' in sample_text or '@' in sample_text:
            metadata['table_type'] = 'contact_list'
            metadata['has_contact_info'] = True
        elif 'section' in sample_text and ('covered' in sample_text or 'benefit' in sample_text):
            metadata['table_type'] = 'benefit_schedule'
        else:
            metadata['table_type'] = 'general'
        
        return metadata
    
    def _create_text_chunk(self, content: str, section_code: str, section_name: str,
                          content_type: str, page_num: int, title: str = "") -> Optional[Chunk]:
        """Create a text chunk with full content preservation."""
        if not content or len(content.strip()) < 30:
            return None
        
        # Clean headers/footers but keep ALL content including contact info
        cleaned_content = self._clean_header_footer(content)
        
        if not cleaned_content or len(cleaned_content) < 30:
            return None
        
        metadata = {
            "section": section_code,
            "subsection": title or section_name,
            "title": section_name,
            "type": content_type,
            "page": page_num,
            "content_format": "text",
            "char_count": len(cleaned_content),
            "word_count": len(cleaned_content.split()),
        }
        
        # Detect if contains contact info
        if any(marker in cleaned_content.lower() for marker in ['tel:', 'fax:', 'email:', '@', 'phone:']):
            metadata['has_contact_info'] = True
        
        return Chunk(
            id=self._generate_id(section_code),
            content=cleaned_content,
            metadata=metadata
        )
    
    def _create_table_chunk(self, markdown_table: str, table_data: List[List[Any]],
                           section_code: str, section_name: str, content_type: str,
                           page_num: int) -> Optional[Chunk]:
        """Create a table chunk with markdown format."""
        if not markdown_table:
            return None
        
        metadata = self._extract_table_metadata(table_data, page_num)
        metadata.update({
            "section": section_code,
            "title": section_name,
            "type": content_type,
            "content_format": "markdown_table",
        })
        
        return Chunk(
            id=self._generate_id(f"{section_code}_TBL"),
            content=markdown_table,
            metadata=metadata
        )
    
    def _split_into_semantic_chunks(self, text: str, section_code: str, 
                                    section_name: str, content_type: str,
                                    page_num: int) -> List[Chunk]:
        """
        Split text into semantic chunks at definition/section boundaries.
        Preserves all content.
        """
        chunks = []
        
        # Pattern to find definition boundaries (Def.1, Def.2, Section X.X, etc.)
        boundary_pattern = r'(?=(?:^|\n)(?:Def\.\d+\.|Section\s+[A-Z]\.\d+(?:\.\d+)*\.?\s|(?:\d+\.){1,3}[A-Z]\s))'
        
        # Split on boundaries
        parts = re.split(boundary_pattern, text)
        
        current_chunk = ""
        current_title = ""
        
        for part in parts:
            if not part or not part.strip():
                continue
            
            # Check if this part starts a new definition/section
            header_match = re.match(r'(Def\.\d+\.|Section\s+[A-Z]\.\d+(?:\.\d+)*\.?|\d+\.\d+\.[A-Z])\s*(.+?)(?=\n|$)', part, re.DOTALL)
            
            if header_match:
                # Save previous chunk
                if current_chunk.strip():
                    chunk = self._create_text_chunk(
                        current_chunk, section_code, section_name, 
                        content_type, page_num, current_title
                    )
                    if chunk:
                        chunks.append(chunk)
                
                # Start new chunk with header
                current_title = header_match.group(1).strip()
                current_chunk = part
            else:
                current_chunk += "\n" + part
            
            # Force split if too large (but try to keep semantic units)
            if len(current_chunk) > 2000:
                chunk = self._create_text_chunk(
                    current_chunk, section_code, section_name,
                    content_type, page_num, current_title
                )
                if chunk:
                    chunks.append(chunk)
                current_chunk = ""
        
        # Don't forget last chunk
        if current_chunk.strip():
            chunk = self._create_text_chunk(
                current_chunk, section_code, section_name,
                content_type, page_num, current_title
            )
            if chunk:
                chunks.append(chunk)
        
        return chunks
    
    def extract_from_pdf(self) -> List[Dict]:
        """
        Main extraction method.
        Processes PDF page by page, preserving tables and all content.
        """
        if not PDFPLUMBER_AVAILABLE:
            raise ImportError("pdfplumber required. Install: pip install pdfplumber")
        
        if not self.pdf_path or not Path(self.pdf_path).exists():
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")
        
        print(f"Processing: {self.pdf_path}")
        
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"Pages: {total_pages}\n")
            
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"Page {page_num:2d}/{total_pages}: ", end="")
                page_chunks = 0
                
                # Extract tables with structure preservation
                tables = page.extract_tables()
                
                for table_idx, table in enumerate(tables):
                    if not table:
                        continue
                    
                    # Convert to markdown
                    markdown_table = self._format_table_to_markdown(table)
                    
                    if markdown_table:
                        # Detect section from table content
                        sample = ' '.join(str(c) for row in table[:2] for c in row if c)
                        section_code, section_name, content_type = self._detect_section(sample, page_num)
                        
                        chunk = self._create_table_chunk(
                            markdown_table, table, section_code, 
                            section_name, content_type, page_num
                        )
                        
                        if chunk:
                            self.chunks.append(chunk)
                            page_chunks += 1
                
                # Extract text (excluding table areas to avoid duplication)
                text = page.extract_text()
                
                if text:
                    # Detect section
                    section_code, section_name, content_type = self._detect_section(text, page_num)
                    
                    # Create semantic chunks
                    text_chunks = self._split_into_semantic_chunks(
                        text, section_code, section_name, content_type, page_num
                    )
                    self.chunks.extend(text_chunks)
                    page_chunks += len(text_chunks)
                
                print(f"{page_chunks} chunks")
        
        print(f"\n{'='*50}")
        print(f"Total chunks created: {len(self.chunks)}")
        print(f"{'='*50}")
        
        return [c.to_dict() for c in self.chunks]
    
    def save_chunks(self, output_path: str = "policy_chunks.json"):
        """Save chunks to JSON."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump([c.to_dict() for c in self.chunks], f, indent=2, ensure_ascii=False)
        print(f"\nSaved to: {output_path}")
        return output_path
    
    def get_statistics(self) -> Dict:
        """Get extraction statistics."""
        stats = {
            "total_chunks": len(self.chunks),
            "by_content_type": {},
            "by_section": {},
            "by_format": {},
            "tables_with_contacts": 0,
            "text_with_contacts": 0,
            "total_chars": 0,
        }
        
        for chunk in self.chunks:
            # Content type
            ct = chunk.metadata.get("type", "unknown")
            stats["by_content_type"][ct] = stats["by_content_type"].get(ct, 0) + 1
            
            # Section
            sec = chunk.metadata.get("section", "unknown")
            stats["by_section"][sec] = stats["by_section"].get(sec, 0) + 1
            
            # Format
            fmt = chunk.metadata.get("content_format", "unknown")
            stats["by_format"][fmt] = stats["by_format"].get(fmt, 0) + 1
            
            # Contact info detection
            if chunk.metadata.get("has_contact_info"):
                if fmt == "markdown_table":
                    stats["tables_with_contacts"] += 1
                else:
                    stats["text_with_contacts"] += 1
            
            stats["total_chars"] += len(chunk.content)
        
        if self.chunks:
            stats["avg_chunk_size"] = stats["total_chars"] // len(self.chunks)
        
        return stats


def main():
    """Example usage."""
    
    # Configuration
    PDF_FILE = "optima-secure-revision-pw (1).pdf"
    OUTPUT_FILE = "hdfc_ergo_policy_chunks.json"
    
    # Create and run chunker
    chunker = PolicyDocumentChunker(pdf_path=PDF_FILE)
    
    try:
        # Extract
        chunks = chunker.extract_from_pdf()
        
        # Statistics
        stats = chunker.get_statistics()
        print("\n--- STATISTICS ---")
        print(f"Total chunks: {stats['total_chunks']}")
        print(f"Average size: {stats.get('avg_chunk_size', 0)} chars")
        print(f"\nBy format:")
        for fmt, count in sorted(stats['by_format'].items()):
            print(f"  {fmt}: {count}")
        print(f"\nBy content type (top 10):")
        for ct, count in sorted(stats['by_content_type'].items(), key=lambda x: -x[1])[:10]:
            print(f"  {ct}: {count}")
        print(f"\nContact info preserved:")
        print(f"  Tables with contacts: {stats['tables_with_contacts']}")
        print(f"  Text with contacts: {stats['text_with_contacts']}")
        
        # Save
        chunker.save_chunks(OUTPUT_FILE)
        
        # Show samples
        print("\n--- SAMPLE CHUNKS ---")
        
        # Find interesting samples
        samples_to_show = [
            ("table", "plan_comparison"),
            ("table", "ombudsman_contacts"),
            ("text", "definitions"),
            ("text", "base_coverage"),
        ]
        
        shown = 0
        for chunk in chunker.chunks:
            if shown >= 6:
                break
            
            fmt = chunk.metadata.get("content_format")
            tbl_type = chunk.metadata.get("table_type", "")
            
            # Check if this matches desired sample
            match = False
            for desired_fmt, desired_type in samples_to_show:
                if fmt == desired_fmt and (desired_type in tbl_type or desired_type in chunk.metadata.get("type", "")):
                    match = True
                    break
            
            if match or (shown < 2 and len(chunk.content) > 200):
                print(f"\n{'='*60}")
                print(f"ID: {chunk.id}")
                print(f"Section: {chunk.metadata.get('section')} | {chunk.metadata.get('title')}")
                print(f"Type: {chunk.metadata.get('type')} | Format: {fmt}")
                print(f"Page: {chunk.metadata.get('page')}")
                if chunk.metadata.get("has_contact_info"):
                    print("⚠️  Contains contact information (preserved)")
                print(f"{'-'*60}")
                
                # Show content preview
                content = chunk.content
                if len(content) > 500:
                    content = content[:500] + "..."
                print(content)
                shown += 1
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()