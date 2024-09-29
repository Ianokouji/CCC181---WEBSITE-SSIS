import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Blueprint,jsonify,request
from backend.models import Program
from pymysql.err import IntegrityError

program_routes = Blueprint('program_routes',__name__)


@program_routes.route('/list',methods=['GET'])
def getPrograms():
    programs = Program.getPrograms()
    return jsonify(programs)

@program_routes.route('/add',methods=['POST'])
def addProgram():
    data = request.json
    Program_Code = data.get("Program_Code")
    Program_Name = data.get("Program_Name")
    College_Code = data.get("College_Code")

    if not Program_Code or not Program_Name or not College_Code:
        return jsonify({"message":"Fields are missing ERROR"}), 400
    
    capitalized_Program_Code = Program_Code.upper()
    try:
        Program.addProgram(capitalized_Program_Code,Program_Name,College_Code)

    except IntegrityError as e:
        if e.args[0] == 1062:
            return jsonify({"message":f"Duplicate entry found in the fields for Program Code {Program_Code}"}),409
        else:
            return jsonify({"message":f"Error! Database error: {str(e)}"}),400
    except Exception as e:
        return jsonify({"message":f"Error in adding Program has occured {str(e)}"}),400

    return jsonify({"message":f"Program with code {Program_Code} Added Successfully"}), 201


@program_routes.route('/update/<ProgramCodeUp>',methods=['PATCH'])
def updateProgram(ProgramCodeUp):
    ProgramToUpdate = Program.getProgram(ProgramCodeUp)

    if not ProgramToUpdate:
        return jsonify({"message":"Program to update does NOT EXIST"}), 404
    
    data = request.json
    Program_Code = data.get("Program_Code",ProgramToUpdate['Program_Code'])
    Program_Name = data.get("Program_Name",ProgramToUpdate['Program_Name'])
    College_Code = data.get("College_Code",ProgramToUpdate['College_Code'])

    capitalized_Program_Code = Program_Code.upper()
    try:
        Program.updateProgram(capitalized_Program_Code,Program_Name,College_Code,ProgramCodeUp)

    except IntegrityError as e:
        if e.args[0] == 1062:
            return jsonify({"message":f"Duplicate entry found in the fields for Program Code {Program_Code}"}),409
        else:
            return jsonify({"message":f"Error! Database error: {str(e)}"}),400
    except Exception as e:
        return jsonify({"message":f"Error in UPDATING Program: {str(e)}"}), 400

    return jsonify({"message":"Program Updated Successfully"}), 200



@program_routes.route('/delete/<ProgramCodeDel>',methods=['DELETE'])
def deleteProgram(ProgramCodeDel):
    ProgramToDelete = Program.getProgram(ProgramCodeDel)

    if not ProgramToDelete:
        return jsonify({"message":"The program to delete does NOT EXIST"}), 404
    
    try:
        Program.deleteProgram(ProgramCodeDel)
    except Exception as e:
        return jsonify({"message":f"Error in DELETING Program: {str(e)}"}),400

    return jsonify({"message":f"Program with Code {ProgramCodeDel} Deleted Successfully"}),200


@program_routes.route('search/<Type>/<SearchQuery>', methods=['GET'])
def searchProgram(Type,SearchQuery):
    if Type == 'P_CODE':
        programs = Program.searchProgramCode(SearchQuery)
    elif Type == 'NAME':
        programs = Program.searchProgramName(SearchQuery)
    elif Type == 'C_CODE':
        programs = Program.searchCollegeCode(SearchQuery)
    else:
        return jsonify([]), 400
    
    return jsonify(programs),200
    