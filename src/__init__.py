from flask import Flask

app=Flask(__name__,static_folder='./resource')
import src.main