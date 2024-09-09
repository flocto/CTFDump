;nyquist plug-in
;version 4
;type process
;name "Dereverb"
;manpage "Dereverb"
;debugbutton true
;preview enabled
;author "JH"
;release 2.4.2-7
;copyright "Released under terms of the GNU General Public License version 2"

;; Released under terms of the GNU General Public License version 2:
;; http://www.gnu.org/licenses/old-licenses/gpl-2.0.html .

;control mode "Choose Mode" choice "Simple, Expert" 0
;control sensitivity "Sensitivity" int "" 10 0 20
;control reduction "Reverb Reduction" float "(dB)" -12 -30 -5
;control text "____________________________________________________________________________________"
;control text "EXPERT SETTINGS"
;control text "You have to select Expert mode to activate these additional settings."
;control attack "    Attack" int "(ms)" 12 1 100
;control release "    Release" int "(ms)" 25 1 100
;control text "          . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
;control text "    High Frequency Band (> 4000 Hz)"
;control 4_band_T_offset "          - Threshold offset" float "(dB)" 0 -10 10
;control 4_band_R_offset "          - Reduction offset" float "(dB)" 0 -10 10
;control text "    High-mid Frequency Band (1400 - 4000 Hz)"
;control 3_band_T_offset "          - Threshold offset" float "(dB)" 0 -10 10
;control 3_band_R_offset "          - Reduction offset" float "(dB)" 0 -10 10
;control text "    Low-mid Frequency Band (400 - 1400 Hz)"
;control 2_band_T_offset "          - Threshold offset" float "(dB)" 0 -10 10
;control 2_band_R_offset "          - Reduction offset" float "(dB)" 0 -10 10
;control text "    Low Frequency Band (< 400 Hz)"
;control 1_band_T_offset "          - Threshold offset" float "(dB)" 0 -10 10
;control 1_band_R_offset "          - Reduction offset" float "(dB)" 0 -10 10

;;; RAM max consumption
(SND-SET-MAX-AUDIO-MEM 2000000000)

;;; Global variables
(cond 
  ((= mode 0)
    (setq attack 12)
    (setq release 25)
    (setq 1_band_T_offset 0)
    (setq 2_band_T_offset 0)
    (setq 3_band_T_offset 0)
    (setq 4_band_T_offset 0)
    (setq 1_band_R_offset 0)
    (setq 2_band_R_offset 0)
    (setq 3_band_R_offset 0)
    (setq 4_band_R_offset 0)))
(setq sensitivity (- (float sensitivity) 10))
(setq attack (/ (float attack) 1000))
(setq release (/ (float release) 1000))
(setq look attack)


;;; Catch errors
(defun error-check ()
  (when (< len 100) ; 100 samples required 
    ;; Work around bug 2012.
    (throw 'err (format nil "~%Insufficient audio selected.~%~
                             Make the selection longer than ~a ms."
                        (round-up (/ 100000 *sound-srate*)))))
  (when (> len 417600000) ; max length can be 2h 25min
    (throw 'err (format nil "~%Too long selection.~%~
                             Make the selection shorter than ~a minutes."
                        (round-down (/ 6960000 *sound-srate*))))))


;;; Utility functions
(defun round-up (num)
  (round (+ num 0.5)))

(defun round-down (num)
  (round (- num 0.5)))

(defun get-rms (params ln)
  ;; Return RMS of mono sound.
  (let ((hpass (nth 0 params))
        (lpass (nth 1 params)))
    (setf step (best-step-size ln))
    (setf ms (snd-avg (mult (filter *track* hpass lpass) 
                            (filter *track* hpass lpass)) step step op-average))
    ;; Use SND-AVG rather than S-AVG for compatibility with
    ;; Audacity versions < 3.0.
    (when (> (snd-length ms 2) 1)
      (setf step (snd-length ms ny:all))
      (setf ms (snd-avg ms step step op-average)))
    (linear-to-db (sqrt (snd-fetch ms)))))

(defun best-step-size (ln)
  ;; Return a step size less than maxblock.
  ;; Optimisation Hints:
  ;; Large step requires less loops in LISP, so may be faster,
  ;; but greater difference between step size and final block length
  ;; decreases precision.
  (let ((maxblocklen 1000000))
    (if (> ln maxblocklen)
        (round (sqrt (float ln)))
        ln)))

(defun filter (sig low high)
  (when low
    (setf sig (highpass8 sig low)))
  (if high
    (lowpass8 sig high)
    sig))
    
(defun noisegate (filtered_sound look attack release reduce threshold)
  (snd-gate (s-abs filtered_sound) 
            look 
            attack 
            release 
            reduce 
            threshold))

;;; Main function
(defun main_process (param_list)
  (error-check)
  (let ((ln (truncate len))
        (output 0))
    (dolist (params param_list output)
      (let ((filtered_sound (filter *track* (nth 0 params) (nth 1 params)))
            (reduce (db-to-linear (+ reduction (nth 2 params))))
            (threshold (db-to-linear (+ (get-rms params ln) 
                                        sensitivity 
                                        (nth 3 params)))))
        (setf output (sum output 
                          (mult filtered_sound 
                                (diff (clip (noisegate filtered_sound 
                                                       look 
                                                       attack 
                                                       release 
                                                       reduce 
                                                       threshold) 1.0) 0))))))))

;;; Run the program
(catch 'err (main_process 
              (list 
                (list nil 400 1_band_R_offset 1_band_T_offset)
                (list 450 1500 2_band_R_offset 2_band_T_offset)
                (list 1330 4000 3_band_R_offset 3_band_T_offset)
                (list 4000 nil 4_band_R_offset 4_band_T_offset))))
                