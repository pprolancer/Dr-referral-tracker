# Practice_Referral

sample_db
username: dradmin
password: drpassword

Travis-CI: 
[![Build Status](https://travis-ci.org/Heteroskedastic/Dr-referral-tracker.svg?branch=master)](https://travis-ci.org/Heteroskedastic/Dr-referral-tracker)    
QuantifiedCode: 
[![Issues](https://www.quantifiedcode.com/api/v1/project/2441b741074344f795cb6203dee0cea7/badge.svg)](https://www.quantifiedcode.com/app/project/2441b741074344f795cb6203dee0cea7)    
CodeCove: 
[![codecov.io](https://codecov.io/github/Heteroskedastic/Dr-referral-tracker/coverage.svg?branch=master)](https://codecov.io/github/Heteroskedastic/Dr-referral-tracker?branch=master)

A simple app designed to allow Medical clinics to easily track patient visits, patient referral sources and treating physician procutivity.

### Model design:

#### Organization
* Name and profile
* Type (Marketing, Insurance, Internal, Work comp., Healthcare Provider)

#### ReferringEntity
(Current patient and Returning patient, will be assigned to the "Internal" Org.)
* OrgForgnkey
* title (optional)
* name
* phone (optional)
* email (optional)


#### PatientVist
* ReferringEntity (key)
* VisitDate
* AppiontmentTime (optional)
* ActualTime (optional)
* TimeStamp

#### TreatingProvider
* Title (optional)
* name
* type (Physician Assistant, Doctor, Nurse, Nurse Pratitioner)
