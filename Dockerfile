FROM koryakinp/mlagents

RUN pipenv install Pillow
RUN pipenv install Keras
RUN pipenv install moviepy
RUN pipenv install Pympler
RUN pipenv install scikit-learn
RUN pipenv install tensorflow==1.13.1
RUN pipenv install easydict
RUN pipenv install gym==0.9.2
RUN pipenv install scikit-image

RUN git clone https://github.com/koryakinp/A2C.git

WORKDIR /python-env/A2C

RUN wget https://github.com/koryakinp/MLDriver/releases/download/5.5/MLDriver_Linux_x86_64.zip
RUN mkdir environments
RUN mkdir experiments
RUN mkdir records
RUN unzip MLDriver_Linux_x86_64.zip -d environments/
RUN rm MLDriver_Linux_x86_64.zip
RUN rm -rf /python-env/mldriver-discrete-steering/environments/__MACOSX

RUN chmod 755 runner.sh

ENTRYPOINT [ "./runner.sh" ]
CMD ["-c mldriver.json"]