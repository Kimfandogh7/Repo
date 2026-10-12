# Persian ASR test (FLEURS fa_ir test, 12 clips, 207 s audio, 2 vCPU GitHub runner)

| model | WER % | RTF | source run |
|---|---|---|---|
| faster-whisper small (int8, beam 1) | 56.25 | 0.565 | run 38260272699 (results in commit d3fadb7) |
| faster-whisper medium (int8, beam 1) | 31.85 | 0.964 | run 38260272699 (results in commit d3fadb7) |
| Shenava Koochik v1.0 (CTC, sherpa-onnx) | 9.52 | 0.013 to 0.045 | runs 38263340618 to 38264023792 |
| Shenava Koochik v1.5 (RNNT, sherpa-onnx) | 10.12 | 0.018 | run 38264023792 |

Notes:
- results.json holds only the last run (Shenava). The whisper rows above come from the earlier run.
- Normalization: diacritics removed, ZWNJ to space, punctuation stripped, Arabic yeh and kaf mapped to Persian.
- Sample is small (12 clips). It is read speech (FLEURS), not video audio.
