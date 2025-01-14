#include <stdio.h>
#include <stdint.h>
#include <math.h>

#define SAMPLE_RATE 44100
#define DURATION 0.1  // 0.1 секунда для клика
#define FREQUENCY 1500  // Частота клика (в герцах)
#define AMPLITUDE 3000  // Амплитуда звука (уменьшенная для негромкого клика)

void write_wav_header(FILE *file, int sample_rate, int num_samples) {
    int byte_rate = sample_rate * sizeof(int16_t);
    int data_size = num_samples * sizeof(int16_t);

    // WAV header
    fwrite("RIFF", 1, 4, file);
    int32_t chunk_size = 36 + data_size;
    fwrite(&chunk_size, 4, 1, file);
    fwrite("WAVE", 1, 4, file);
    
    // fmt subchunk
    fwrite("fmt ", 1, 4, file);
    int32_t subchunk1_size = 16;
    fwrite(&subchunk1_size, 4, 1, file);
    int16_t audio_format = 1;  // PCM
    fwrite(&audio_format, 2, 1, file);
    int16_t num_channels = 1;  // Mono
    fwrite(&num_channels, 2, 1, file);
    fwrite(&sample_rate, 4, 1, file);
    fwrite(&byte_rate, 4, 1, file);
    int16_t block_align = sizeof(int16_t);
    fwrite(&block_align, 2, 1, file);
    int16_t bits_per_sample = 16;
    fwrite(&bits_per_sample, 2, 1, file);

    // data subchunk
    fwrite("data", 1, 4, file);
    fwrite(&data_size, 4, 1, file);
}

int main() {
    FILE *file = fopen("click.wav", "wb");

    int num_samples = (int)(SAMPLE_RATE * DURATION);
    write_wav_header(file, SAMPLE_RATE, num_samples);

    for (int i = 0; i < num_samples; i++) {
        // Генерируем простую затухающую синусоиду для клика
        double t = (double)i / SAMPLE_RATE;
        double envelope = exp(-t * 10);  // Быстрое затухание
        int16_t sample = (int16_t)(AMPLITUDE * sin(2.0 * M_PI * FREQUENCY * t) * envelope);
        fwrite(&sample, sizeof(int16_t), 1, file);
    }

    fclose(file);
    return 0;
}

