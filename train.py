from datasets import load_dataset
import json
DATASET = load_dataset("allenai/qasper")

def main():
    outputObject = []
    train = DATASET["train"]
    for paperIndex, eachTrain in enumerate(train):
        dictionary = {}
        dictionary["paper_index"] = paperIndex
        dictionary["title"] = eachTrain["title"]
        full_text = eachTrain["full_text"]["paragraphs"]
        flatten = flatten_list(full_text)
        flatten = [item for item in flatten if item]
        
        # dictionary["passages"] = flatten
        
        questions = eachTrain["qas"]["question"]
        answersPerQuestion = eachTrain["qas"]["answers"]
        
        numQuestions = len(questions)                              
        qasArray = []
        questionDictionary = {}

        for i in range(numQuestions):
            evidenceIndexArray = []
            currentQuestion = questions[i]
            answers = answersPerQuestion[i]
            
            for eachAnswer in answers["answer"]:
                unanswerable = eachAnswer["unanswerable"]
                if unanswerable == False:
                        
                    allEvidence = eachAnswer["evidence"]
                    for evidenceIndex, eachEvidence in enumerate(allEvidence):
                        if eachEvidence in flatten:
                            # evidenceIndexArray.append(flatten.index(eachEvidence))
                            evidenceIndexArray.append(eachEvidence)
            
            evidenceIndexArray = list(set(evidenceIndexArray))
            if len(evidenceIndexArray) > 0: # question has answers
                questionDictionary = {}
                questionDictionary["question"] = currentQuestion
                print(currentQuestion)

                # include answer in json
                answer_list = []
                for eachAnswer in answers["answer"]:
                    if eachAnswer["unanswerable"] == False:
                        if eachAnswer["yes_no"] != None:
                            answer = eachAnswer["yes_no"]
                        elif eachAnswer["free_form_answer"] != "": 
                            answer = eachAnswer["free_form_answer"]
                        else:
                            answer = eachAnswer["extractive_spans"]
                        
                        print(f'{answer}')
                        answer_list.append(answer)
                
                print(answers)
                questionDictionary["answer"] = answer_list
                        
                questionDictionary["evidence"] = evidenceIndexArray

                qasArray.append(questionDictionary)
                  
                
        if len(qasArray) > 0:
            dictionary["qas"] = qasArray
            outputObject.append(dictionary)  
    
    export(outputObject)
       
def flatten_list(nested_list):
    flattened = []
    for item in nested_list:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)
    return flattened

def export(data):
    output_file = "output.json"
    with open(output_file, "w") as file:
        json.dump(data, file, indent=1)

    print(f"Data exported to {output_file}")

main()