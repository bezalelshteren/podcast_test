# podcast_test

### I will try to explain the process and the way of thinking and the way in which the system we were asked to create works.

## The utils folder contains

everything needed for several containers
It contains the file that reads from the path and the file that converts the path into binary and the file that generates hash
and the producer and consumer that reads and writes to Kafka and the file that manages the connection to ELASTIC and reads from it,
updates and inserts

## And in the manager_the_read_and_send folder

there is the file that generates the metadata and the file that manages everything
And it uses the UTILS files because it works like this it reads all the files from the path and
transfers it to the file that generates the metadata that adds the metadata to each podcast such as the name of the file, the size,
the production date and then it sends to Kafka

## And in the manage_consumer_and_writing_to_mongo_and_elastic folder 

there is the file that writes to Mongo and the manager of this service
And it also uses the UTILS files because it reads from Kafka and converts the The podcast is binary and generates a HASH based on the binary,
and this is the ID, and so it writes to Mongo with the ID I created the entire contents of the binary file.
And with that ID, it writes to ELASTICSEARCH the metadata.

## And the convert_text_to_speach folder contains
the file that converts audio to text, the file that sends the text to Kafka,
and the file that reads the text from Kafka and updates the text of the podcast in each document. 
And it works like this. It's like starting everything from the beginning because it reads the path and makes a HASH on the binary,
then goes to the document in Elastic whose HASH is the same as the HASH it created and adds the text there.

I was basically debating whether to go and read the binary from Mongo and convert it to text, and then insert it into Elastic because it doesn't do the process of reading from the path on the computer or in the container again, and it's more of a single pipeline system that does everything.

But from the requirement we received, I understood that it was an unrelated system because it is a system The reason for this is because the researchers are sick, so I deduced that it should be a separate service that is not dependent on the first service at all, and that converting the audio to text takes a long time, so they work in parallel, and it doesn't wait for the first system to write to Mongo and only then start reading from there.

Then there is the container processes_and_enrich, which waits until the container that writes the text to Elastic finishes, then it reads the content of the text and checks the risk level based on a calculation of the number of dangerous words divided by the length of the text and adds the field. It first holds a risk level variable, which is the number of dangerous words in each index divided by the number of words there are. Then I divide the risk level by 4. If it is in the lower quarter, then it is not dangerous. And in the is_bds field, it will be FALSE, otherwise it is TRUE. Then in the bds_threat_level field, I check if it is in the upper quarter, it is really dangerous, in the middle, it is less, and so on. And in the bds_percent field, I put the score of the number of dangerous words in relation to the entire length of the text.

## Then I log the file. 
Which sends to Elastic all the logs that were saved throughout the project.
I wrote a lot of logs for every small process that happens so that we can know exactly what worked and what failed and why.