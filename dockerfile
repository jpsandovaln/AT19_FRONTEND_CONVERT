#
# @dockerfile Copyright (c) 2023 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved.
#
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft. 

FROM python:3.10-alpine3.15

WORKDIR /

RUN apk update \
    apk add --no-cache python3-dev\&& pip install --upgrade pip

COPY AT19_FRONTEND_CONVERT/. /

RUN apk update
RUN apk upgrade
RUN pip install -r requirements.txt

RUN python WEB-CONVERTER/src/com/jalasoft/Web-converter/app.py

CMD ["python", "WEB-CONVERTER/src/com/jalasoft/Web-converter/app.py"]