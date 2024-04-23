import grpc
import audio_pb2
import audio_pb2_grpc
import pyaudio

def streamAudio(stub, fileName):
    response = stub.downloadAudio(
        audio_pb2.DownloadFileRequest(name=fileName)
    )

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=2, rate=40000, output=True)

    print("Reproduciendo el archivo: " + fileName)
    for audio_chunk in response:
        print(".", end="", flush=True)
        stream.write(audio_chunk.data)

    print("\nRecepción de datos correcta.")
    print("Reproducción terminada", end="\n\n")

def run():
    port = "8080"
    channel = grpc.insecure_channel("localhost:" + port)
    stub = audio_pb2_grpc.AudioServiceStub(channel)

    try:
        fileName = "anyma.wav"
        streamAudio(stub, fileName)
    except KeyboardInterrupt:
        pass
    finally:
        channel.close()

if __name__ == "__main__":
    run()


