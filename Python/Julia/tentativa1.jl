# run() --> por comandos do terminal aqui
# run(`echo 'modifing text file to desired format'`)
# println("Modifing text file to desired format....")
# run(`bash /home/labic-redbull/.julia/v0.5/AdaGram/utils/tokenize.sh input_text clean_text`)
# println("Done!")
# print("Creating a dictionary....")
# run(`bash /home/labic-redbull/.julia/v0.5/AdaGram/utils/dictionary.sh clean_text dictionary_file`)
# println("Done!")
# print("Creating model....")
# run(`jbash /home/labic-redbull/.julia/v0.5/AdaGram/train.jl clean_text dictionary_file trained_file`)

# println("Done!")


NUMBER_NEIGHBORS=5
THRESHOLD = 0.4
using AdaGram
import JSON
# using HDF5, JLD



# GETTING TAINED FULE
trained_file_path = split(Base.source_path(),'/')
trained_file_path[end] = ARGS[1]
# println(trained_file_path)
trained_file_path = join(trained_file_path,'/')
vm, dict = load_model(trained_file_path);

open("clean_port_dict.json", "r") do f
    global sentiment_dict
    dicttxt = readstring(f)  # file information to string
    sentiment_dict=JSON.parse(dicttxt)  # parse and transform data
    # println(eltype(sentiment_dict))
    # print(sentiment_dict["cumulus"])
end


function print_words()
  open("words_trained.txt","w") do word_list
    for word in dict.word2id
      write(word_list, string(word[1],"\n"))
    end
  end

end
function analyse_word(word)
  possible_meanings = expected_pi(vm, dict.word2id[word])
  number_of_probable =length(possible_meanings[possible_meanings .> THRESHOLD])
  possible_meanings=sort(possible_meanings,rev=true)
  probable_meanings = possible_meanings[1:number_of_probable]
  print("In analyse_word(): ")
  println(probable_meanings)
  # println(sentiment_dict)
  for meaning = (1:number_of_probable)
  	# print(eltype(word))
   	neighbors = nearest_neighbors(vm, dict, word, meaning, NUMBER_NEIGHBORS)

    neighbors_sentiment_dict=Dict("anger"=>0,
      "anticipation"=>0,
      "disgust"=>0,
      "fear"=>0,
      "joy"=>0,
      "negative"=>0,
      "positive"=>0,
      "sadness"=>0,
      "surprise"=>0,
      "trust"=>0)

    for neighbor_name in neighbors
      print("neighbor")
      println(neighbor_name)

      neighbor=get(sentiment_dict, neighbor_name[1], "não tem")
      if neighbor != "não tem"

        for sentiment in keys(neighbors_sentiment_dict)

          sentiment_value=parse(Float64,neighbor[sentiment][1])
          print("sentiment value: ")
          println(sentiment_value)
            # sentiment_value
          # neighbors_sentiment_dict[sentiment]=neighbors_sentiment_dict[sentiment]+sentiment_value
          neighbors_sentiment_dict[sentiment]+=sentiment_value

          println(sentiment)
        end
      end
   	end
    for sentiment in keys(neighbors_sentiment_dict)
      println(neighbors_sentiment_dict[sentiment])
    end
  end
end
# println(analyse_word("the"))

print_words()
analyse_word(ARGS[2])

# print(vm)
# word = "the"
# significados = expected_pi(vm, dict.word2id[word])
# # println(significados)
# # println(length(significados[significados .> 0.1]))
# relevantes = length(significados[significados .> 0.1])
# for x = (1:relevantes)
# 	println("Word $word \t Meaning $x")
# 	vizinhos = nearest_neighbors(vm, dict, word, x, 5)
# 	println(vizinhos)
# end



