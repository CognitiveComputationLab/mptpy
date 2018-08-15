;;; Program modeling the theory of the selection task (based on algorithm in J-L and Wason, 1970) - J-L Nov 2016.

#| The high-level fn is: selection.  
   To run selection for modeling, call-selection with values that will be assigned to three global variables:
    *converse*          - if called selection scans mental model in both directions 
    *examine-all-cards* - if called program examines all four cards, and if card can't verify then tests whether falsifies
    *falsification*     - only choses those cards that falsify. It has no effect unless examine-all-cards is elicited.
 Example (call-selection .5 .2 .1 20) -- runs that setting for 20 trials 
 By default, the cards are ((p)(- p)(q)(- q)) and the rule is (if p then q).  The rule can be changed to '(iff p then q)  |#
(defun call-selection(converse examine-all-cards falsification no-of-trials &optional rule cards)
  (setf *converse* converse *examine-all-cards* examine-all-cards *falsification* falsification)
  (dotimes (count no-of-trials)
    (print (selection))))

; Illustrates the program and can be used with verbose tracer
(defun test-selection(&optional rule cards &key (verbose t))
  (initialize-tracer :verbose t)
  (setf *converse* 1 *examine-all-cards* 0 *falsification* 0)
  (terpri)
  (trc "Values 1." (format nil "Considers converse, but neither examines all cards nor falsifies."))
  (trc "" (format nil " ~A" (selection rule cards)))                                                           ; => p q

 ; (reset-tracer)
  (setf *converse* 0 *examine-all-cards* 0 *falsification* 0)
  (terpri)
  (trc "Values 2." (format nil "Does not consider converse, and neither examines all cards nor falsifies."))  ; => p
  (trc "" (format nil " ~A" (selection rule cards)))  
 
  ; (reset-tracer)
  (setf *converse* 1 *examine-all-cards* 1 *falsification* 0)
  (terpri)
  (trc "Values 3." (format nil "Considers converse but considers whether all cards that can't verify can falsify."))
  (trc "" (format nil " ~A" (selection rule cards )))                                                  ; => p q -q

  (setf *converse* 0 *examine-all-cards* 1 *falsification* 0)
  (terpri)
  (trc "Values 4." (format nil "Does not consider converse, but considers whether all cards that can't verify can falsify."))
  (trc "" (format nil " ~A" (selection rule cards)))

 ; (reset-tracer)
  (setf *converse* 1  *examine-all-cards* 1  *falsification* 1)
  (terpri)
  (trc "Value 5." (format nil "Considers converse, examines all cards, and falsifies."))
  (trc "" (format nil " ~A" (selection rule cards)))                                                 ; => p -q

  (setf *converse* 0 *examine-all-cards* 1 *falsification* 1)
  (terpri)
  (trc "Value 6." (format nil "Does not consider converse, examines all cards, and falsifies."))
  (trc "" (format nil " ~A" (selection rule cards))))

(defun selection(&optional rule cards &key (verbose t))
  "efficient version of same theory as in J-L & Wason 1970"
  (if (null cards)(setf cards '((p)(- p)(q)(- q))))
  (if (null rule) (setf rule '(if p then q)))
  (let* ((LIS (make-lis rule (insight? *converse*))) models cards-to-select temp
         (remaining-cards (remove-lis1-from-lis2 LIS cards)))
    (trc "[4 5]" (format nil "Examine them one by one."))
    (setf *system* 1 models (parse rule) cards-to-select (new-verify? LIS models))
    (trace-models "Mental model of rule:" models)
    (setf LIS (remove-lis1-from-lis2 cards-to-select LIS))
    (cond((insight? *examine-all-cards*)
              (setf LIS remaining-cards)
              (trc "[13, 14]" (format nil "Insight to examine all cards including ~A" LIS))
              (cond((insight? *falsification*)(trc "[7]" (format nil "Insight to test whether cards could only falsify.")) 
                      (exit-new (falsify? cards rule)))              
                   (t (trc "[7]" (format nil "No insight to test whether cards could only falsify."))
                      (cond((setf remaining-cards (new-verify? LIS models))  
                              (exit-new (append cards-to-select remaining-cards)))
                           (t (trc "[6]" (format nil "They can't verify so check whether they could falsify."))
                              (exit-new (append cards-to-select (falsify? LIS rule))))))))
                            ;  (trc "[16]" (format nil "Select the following cards:"))  cards-to-select)))))
         (t (exit-new cards-to-select)))))

(defun exit-new(cards)
  (trc "[16]" (format nil "Select the following cards:")) cards)

(defun new-verify?(LIS models)
  (let (cards-to-select)
    (dolist(card LIS cards-to-select)
      (if (could-verify? card models)
          (setf cards-to-select (append cards-to-select (list card)))))
    (cond( cards-to-select
            (trc "[6]" (format nil "Verify? yields cards-to-select: ~A" cards-to-select))))
    cards-to-select))

(defvar *system* 1)               ; global for system 1 or 2
(defvar *converse* .99)           ; global for probability of scanning model in both directions
(defvar *examine-all-cards* .99)  ; global for probability of examining all cars
(defvar *falsification* .99)      ; global for only selecting cards that can falsify

(defun insight?(global)
  (< (random-probability) global))

(defun verify?(lis-of-cards rule)
  (let (models cards-to-select)
    (setf *system* 1 models (parse rule))
    (dolist(card lis-of-cards cards-to-select)
      (if (could-verify? card models)
          (setf cards-to-select (append cards-to-select (list card)))))
    (cond( cards-to-select
            (trc "[6]" (format nil "Verify? yields cards-to-select: ~A" cards-to-select))))
    cards-to-select))

(defun could-verify?(card models)
  "rtns card iff it occurs in a model in models"
  (dolist(mod models)
    (if (member-lis card mod)
        (return card))))

(defun falsification-insight?()
  (if (< (random-probability) *falsification*) 
      t))

(defun falsify?(lis-of-cards rule)
  "ok rtns only those cards in lis-of-cards that could falsify the rule"
  (let (models cards-to-select)
    (setf *system* 2 models (parse rule))
    (trace-models "Fully explicit models of rule:" models)
    (dolist (card lis-of-cards cards-to-select)
      (if (could-falsify? card models)
          (setf cards-to-select (append cards-to-select (list card)))))
    (cond( cards-to-select
            (trc "[8]" (format nil "Falsify? yields cards to select."))))
    cards-to-select))

(defun could-falsify?(card models)
  (let ((false-fems (comp models (allpos (car models)))))
     (dolist(mod false-fems)
       (if (member-lis card mod)
           (return card)))))

(defun make-lis(rule converse?)
    (if converse?    
        (setf lis (find-literals rule))
      (setf lis (list (first (find-literals rule)))))
    (trc "[1 2 3]" (format nil "List of potential selections: ~A" lis))
    lis)

(defun find-literals(rule)
  "ok rtns list of literals from rules, converting 'not in rule to '- in resulting literal"
  (let ((itm (car rule)))
  (cond((null rule) nil)
       ((and (equal itm 'not)(variablep (cadr rule)))
              (cons (list '- (cadr rule))(find-literals (cddr rule))))
       ((variablep itm)(cons (list itm)(find-literals (cdr rule))))
       (t (find-literals (cdr rule))))))

(defun remove-lis1-from-lis2(lis1 lis2)
  "ok removes each item in mod1 from mod2"
  (if (null lis1) 
      lis2
    (remove-lis1-from-lis2 (cdr lis1)(remove-literal (car lis1) lis2))))

(defun remove-literal(lit lis)
  "ok removes first and only occurrence of literal from lis"
  (cond((null lis) nil)
       ((not (equal (car lis) lit))(cons (car lis)(remove-literal lit (cdr lis))))
       (t (cdr lis))))
              
;;;;;  Low-level functions
(defun random-probability()
  (/ (random 100) 100.0))

(defun variablep(itm)
  "rtns itm iff it is a *variable*"
  (if (member itm *variables*)
      itm))

(defvar *variables* '(p q))
        
#|
The 1970 algorithm
LIS is potential list of cards to select
Input rule + cards + truth table?
Typical rules '(if a then b)  '(if not a then not b) '(a or not b))

0. (selection cards rule)
    [1, 2, 3] make-lis list-of-potentials  remaining-cards
    loop1
[4,5]:if list-of-potentials
        if 6: setf cards-to-select (verify? list-of-potentials)
           if 7: falification-insight 
                loop2
                8: if setf cards-to-select (falsify? cards-to-select)
                      9: if rule-falsified? card 11:(rtn "rule is false").
                         else 10: (remove cards-to-select list-of-potentials)(go loop1).
                   else 12 "card irrelevant" (remove from list-of-potentials)(go loop1).
           else add to cards to select 10: (remove from list-of-possibilities)(go loop1).
         else (go loop2)
      else if [13, 14] (examine-more? remaining-cards)
                         15: put them on cards-to-select (go loop1)
            else rtn [16] cards to select

(defun 1970-selection(cards rule &key (verbose t))
  "implementation of algorithm in J-L & Wason 1970"
  (let* ((list-of-potentials (make-lis rule (insight? *converse*)))
         (remaining-cards (remove-lis1-from-lis2 list-of-potentials cards))
         (falsification? (insight? *falsification*))(all-cards-insight? (insight? *examine-all-cards*)) cards-to-select
         current-cards)
    (prog()
      loop
      (cond(list-of-potentials (trc "[4 5]" (format nil "Examine them one by one."))
             (cond((setf current-cards (verify? list-of-potentials rule))
                     (setf cards-to-select current-cards)
                     (setf list-of-potentials (remove-lis1-from-lis2 cards-to-select list-of-potentials))
                     (cond( falsification? (trc "[7]" (format nil "Insight to test whether cards could falsify."))
                              (cond((setf cards-to-select (falsify? cards-to-select rule))
                                     (setf list-of-potentials (remove-lis1-from-lis2 cards-to-select list-of-potentials))
                                     (go loop))
                                   (t (trc "[12]" "because these cards are irrelevant: ~A" cards-to-select)
                                      (remove-lis1-from-lis2 cards-to-select list-of-potentials)(go loop))))
                          (t (trc "[10]" (format nil "No insight to falsify."))
                             (remove-lis1-from-lis2 cards-to-select list-of-potentials)(go loop))))
                  (t (trc "[6]" (format nil "They can't verify so check whether they could falsify."))
                     (setf cards-to-select (append cards-to-select (falsify? list-of-potentials rule)))
                     (setf list-of-potentials (remove-lis1-from-lis2 cards-to-select list-of-potentials))
                     (trc "[16]" (format nil "Select the following cards:"))(return cards-to-select))))
           ( all-cards-insight?
                (setf list-of-potentials remaining-cards)
                (trc "[13, 14]" (format nil "Insight to examine all cards including ~A" list-of-potentials))(go loop))
           (t (trc "[16]" (format nil "Select the following cards:"))(return cards-to-select)))))) |#

;---------------------------------------------------------------------------------------------------------------------------
;                                       Part 2: TRACER CLASSES AND FUNCTIONS (Sunny's code)
;---------------------------------------------------------------------------------------------------------------------------

(defclass tracer ()
  ((enabled       :accessor enabled        :initarg :e   :initform nil)
   (steps         :accessor steps          :initarg :s   :initform -1)
   (verbose       :accessor verbose        :initarg :v   :initform nil)
   (runtime       :accessor runtime        :initarg :r   :initform (get-internal-run-time))
   (response      :accessor response       :initarg :res :initform nil)
   (initial-model :accessor initial-model  :initarg :im  :initform nil)
   (final-model   :accessor final-model    :initarg :fm  :initform nil)
   (num-models    :accessor num-models     :initarg :nm  :initform nil)   ; for number of models
   (trace         :accessor trace-output   :initarg :tr  :initform nil))
  (:documentation "Class for tracer logging"))

(defparameter *tracer* (make-instance 'tracer))

(defun compute-runtime ()
  "Converts runtime to process cycle"
  (- (get-internal-run-time) (runtime *tracer*)))

(defun trace-header ()
  "Adds header to system trace on initial output of tracer and on every tracer reset"
  (case (steps *tracer*)
    (-1
     (format t "---- --------- --------------------------------------------------------------------------- ------- ~%")
     (format t "Step System    Description                                                                 Runtime    ~%")
     (format t "---- --------- --------------------------------------------------------------------------- ------- ~%")
     (setf (runtime *tracer*) (get-internal-run-time))
     (incf (steps *tracer*))
     (format t "~4@<~A~> ~9@<~A~> ~75@<~A~> ~7@<~A~>~%"
             (steps *tracer*) "--" "Initialized trace" (compute-runtime)))
    (0
     (format t "---- --------- --------------------------------------------------------------------------- ------- ~%")
     (setf (runtime *tracer*) (get-internal-run-time))
     (format t "~4@<~A~> ~9@<~A~> ~75@<~A~> ~7@<~A~>~%"
             (steps *tracer*) "--" "Reset trace" (compute-runtime)))))

(defun tracer (system description &key (model nil))
  "Fn to add a line to the system trace and optionally print it out"
  (let ((model (cond
                ((null model) nil)
                ((listp model) (mapcar #'copy-class-instance model))
                (model         (copy-class-instance model)))))
    (when (enabled *tracer*)
        (when (member system (list "System 0" "System 1" "System 2" "System 3" "Control" "Language") :test #'string-equal)
          (incf (steps *tracer*)))
        (push (list (if (string-equal system "") "" (steps *tracer*)) system description (compute-runtime) model)
              (trace-output *tracer*))
      (when (verbose *tracer*)
        (trace-header)
        (format t "~4@<~A~> ~9@<~A~> ~75@<~A~> ~7@<~A~>~%" (if (string-equal system "") "" (steps *tracer*))
                system description (compute-runtime))))))

(defun trc (system description &key (m nil))
  "Abbreviation wrapper fn for tracer"
  (tracer system description :model m))

(defun initialize-tracer (&key (enabled t) (steps 1) (verbose t) (runtime (get-internal-run-time)))
  "Initializes tracer to defaults based on parameters"
  (setf *tracer* (make-instance 'tracer :e enabled :s steps :v verbose :r runtime)))

(defun enable-tracer (&key (verbose nil))
  "Enables tracer and sets trace verbosity"
  (if *tracer*
      (progn
        (setf (enabled *tracer*) t)
        (setf (verbose *tracer*) verbose))
    (initialize-tracer :v verbose)))

(defun disable-tracer ()
  "Disables tracer"
  (setf (enabled *tracer*) nil))

(defun reset-tracer ()
  "Resets tracer"
  (unless (< (steps *tracer*) 0)
    (setf (steps *tracer*) -1))
  (setf (trace-output *tracer*) nil)
  (setf (response *tracer*) nil)
  (setf (initial-model *tracer*) nil)
  (setf (final-model *tracer*) nil)
  (setf (runtime *tracer*) (get-internal-run-time))
  *tracer*)

(defun trace-models (text models)
  "Outputs model in tracer format"
  (let (lines
        (output (make-array 0
                            :element-type 'character 
                            :adjustable t 
                            :fill-pointer 0)))
    (with-output-to-string (o output)
      (print-models models :output o))
    (setf lines (rest (cl-utilities::split-sequence (format nil "~%") output)))
    (trc "Printer" text)
    (dolist (line lines)
      (trc "" line))))

;---------------------------------------------------------------------------------------------------------------------------
;                    Part 2: PRINT MODELS
;---------------------------------------------------------------------------------------------------------------------------

; Prints footnotes in print-models if set to t
(defvar *print-footnotes* nil)

(defun print-lis-models(models-lis)
  "prints list of models with appropriate spacing to make regular columns"
  (dolist(models models-lis)
    (print-models models)(terpri)(terpri)))

(defun print-models (models &key (output *standard-output*))
  "prints a set of models properly aligned"
  (setf models (tidy-up models))
  (let ((template (make-print-template models)))
  (cond((null models)(print-sentence '(null model)))
       ((eq models t)(print t))
       (t (dolist(mod models)
            (terpri output)
            (cond((and (not *print-footnotes*)(wholly-implicit mod))
                      (prin-space (center-impl-mod template) output)(princ ". . ." output))
                 (t (pm template mod output))))))))  

(defun pm (template model &optional (output *standard-output*))
  "uses template to print items in model with appropriate separations"
  (let ((lead-in 4))
  (cond((null model) t)
       ((null template)
        (prin-item (car model) output)
        (pm template (cdr model) output))    
       ((and (footnotep (car template))(footnotep (car model)))                       
        (prin-item (car model) output)
        (pm (cdr template)(cdr model) output))
       ((equal (affirm (first template))(affirm (first model)))                 
        (prin-item (car model) output)
        (pm (cdr template)(cdr model) output))
       ((match (affirm (car template))(affirm-mod model))
        (pm template (append-mods (cdr model)(list(car model))) output))
       (t  (prin-space (+ lead-in (length (symbol-name (caar template)))) output)
           (pm (cdr template) model output)))))

(defun center-impl-mod(template)
  "rtns number of spaces to print in order to center . . . for implicit model, depending on template"
  (let ((num 0))
  (dolist(item template num)
    (setf num (+ num 2 (length (symbol-name (first item))))))
  (floor (/ num 2))))

(defun make-print-template(models)
  "lists all literals in models, making them affirmative, and ignoring footnotes, then adds one if there is one 
   in models, treating all bound variables as though they were the same."
  (let* ((temp (affirm-mod (findatms models)))(impl-var (includes-implicit temp))(temp (rem-bound-vars temp)))
    (if  impl-var 
        (append temp (car (modelize impl-var)))
      temp)))
     
(defun rem-bound-vars(model)
  "removes all bound-variables from models, incl those of the form '(- t23) "
  (cond((null model) nil)
       ((eq (caar model) '-)
         (cond((boundp (cadar model))(rem-bound-vars (cdr model)))
              (t (cons (car model)(rem-bound-vars (cdr model))))))
       ((boundp (caar model))(rem-bound-vars (cdr model)))
       (t (cons (car model)(rem-bound-vars (cdr model))))))

(defun prin-item (item &optional (output *standard-output*))
  "prints single prop e.g. '(a1) '(- a1) or '(t121) which is a gentemp variable"
(cond((null item) t)
     ((eq (car item) '-)
           (prin-space 2 output)(princ "\AC " output)(princ (cadr item) output))
     ((boundp (car item))
        (cond( *print-footnotes*
               (princ " " output)(princ "{" output)(princ (car item) output)(princ " " output)(princ (eval(car item)) output)(princ "}" output))))
     (t (prin-space 4 output)(princ (car item) output))))

(defun affirm-mod(mod)
  "changes all items in a model to affirmative"
  (mapcar #'affirm mod))

(defun affirm (itm)
  "rtns affirmative itm if neg, otherwise the affirmative itm"
  (if (eq '- (car itm))
      (negate itm)
     itm))

(defun negate-premise(premise)
  "converts negative sentence to affirmative and vice versa"
  (cond((match 'not premise)(rem-atom 'not premise))
       ((> (length premise) 1)(append '(not comma) premise))
       (t (cons 'not premise))))

(defun prin-space(number &optional (output *standard-output*))
  "prints number of spaces"
  (cond((<= number 0) t)
       (t  (format output " ")                      
           (prin-space (- number 1) output))))     



;---------------------------------------------------------------------------------------------------------------------------
;                    Part 4: GRID SEARCH TO FIND OPTIMAL VALUES OF PARAMETERS TO FIT DATA -- SSK
;---------------------------------------------------------------------------------------------------------------------------

; Discrete parameter settings for grid-search for *converse* *examine-all-cards* *falsification*
(defparameter *parameters* (let ((parameters nil))
                             (dolist (c '(0.0 0.2 0.4 0.6 0.8 1.0))
                               (dolist (e '(0.0 0.2 0.4 0.6 0.8 1.0))
                                 (dolist (f '(0.0 0.2 0.4 0.6 0.8 1.0))
                                   (push (list c e f) parameters))))
                             parameters))

; eg (parameter-search *hinterecker-et-al-2016-exp1* :N 5 :verbose nil)
(defun parameter-search (problems &key (directory nil) (N 1000) (parameters *parameters*) (verbose t))
  "top fn for modeling data"
  (let ((c *converse*) (e *examine-all-cards*) (f *falsification*)
        experiments)
    (if (listp parameters)
        (setf experiments (length parameters))
      (progn
        (setf experiments parameters)
        (setf parameters (randomize *parameters*))))
    #+lispworks (when (not directory) (setf directory (capi:prompt-for-directory "Save data file here:")))
    (format t "~%Exporting data to: ~A~%" directory)
    (dotimes (i experiments)
      (run-experiment problems :N N :verbose verbose :parameters (nth i parameters) :status (list (1+ i) experiments))
      (export-synthetic-data *synthetic-data* :directory directory :parameter-string (format nil "g~A-p~A-s~A" *converse* *examine-all-cards* *falsification*)))
    (setf *converse* c *examine-all-cards* e *falsification* f)))

#|
 (run-experiment *hinterecker-et-al-2016-exp1* :n 2) => makes synthetic data for 2 participants, such as:
rtns data-point
   0     1   2   3     4          5               6          7   9    9   10
                                                                          actual freqs in results
                                                                            |
(("S2" "P4" YES "NA" "NA" ((A OR B) (A ORE B)) IT-FOLLOWS? 0.01 0.01 0.01  24) 
 ("S2" "P3" NO "NA" "NA" ((A ORE B) (A OR B)) IT-FOLLOWS? 0.01 0.01 0.01 3) 
 ("S2" "P2" CONTRADICTION "NA" "NA" ((A ORE B) (A AND B)) POSSIBLE? 0.01 0.01 0.01 10) 
 ("S2" "P1" YES "NA" "NA" ((A OR B) (A AND B)) POSSIBLE? 0.01 0.01 0.01 82)
|#
(defun run-experiment (problems &key (N 20) (verbose t) (parameters nil) (status nil))
  (setf *synthetic-data* nil)

  (when verbose
    (format t "~%--------------------------~%~
               Experiment ~A~%~
               --------------------------~%~
               Problems:            ~5d~%~
               Simulated subjects:  ~5d~%~%" (if status (format nil "(~A of ~A)" (first status) (second status)) "") (length problems) N))

  (dotimes (subject N)
    (dotimes (problem (length problems))
      (let ((problem-list (nth problem problems))
            (data-point   (make-list 11 :initial-element "NA")))

        (run-problem problem-list :parameters parameters)
        (setf (nth 0  data-point) (format nil "S~A" (1+ subject)))   ; subject number
        (setf (nth 1  data-point) (format nil "P~A" (1+ problem)))   ; problem number
        (setf (nth 2  data-point) (response *tracer*))               ; predicted response
        (setf (nth 3  data-point) "NA")                              ; !!! SSK serialize premise models
        (setf (nth 4  data-point) "NA")                              ; !!! SSK serialize conclusion models
        (setf (nth 5  data-point) (first problem-list))              ; CARDS
        (setf (nth 6  data-point) (second problem-list))             ; RULE
        (setf (nth 7  data-point) *converse*)
        (setf (nth 8  data-point) *examine-all-cards*)
        (setf (nth 9  data-point) *falsification*)
        (setf (nth 10 data-point) (third problem-list))              ; actual frequency in real data
        (push data-point *synthetic-data*))) )
  (when verbose
    (format t "Parameter settings:~%~
               ~T           converse   = ~4d~%~
               ~T           examine-all-cards     = ~4d~%~
               ~T           falsification   = ~4d~%~
               --------------------------~%"  *converse* *examine-all-cards* *falsification*)))

(defun export-synthetic-data (data &key (directory nil) (parameter-string nil))
  (multiple-value-bind (second minute hour date month year day-of-week dst-p tz)
      (get-decoded-time)
    
    #+lispworks (when (not directory) (setf directory (capi:prompt-for-directory "Save data file here:")))
  
    (when directory
      (setf pathname (merge-pathnames directory (if (null parameter-string)
                                                    (format nil "SelectiontaskData ~A-~A-~A.csv" year month date)
                                                  (format nil "SelectiontaskData ~A-~A-~A ~A.csv" year month date parameter-string))))
      (with-open-file (output pathname
                              :direction :output
                              :if-exists :supersede
                              :if-does-not-exist :create)
        (format output "Subject,ProblemNumber,Response,PremiseModels,ConclusionModels,Premises,Task,converse,examine-all-cards,falsification,Data~%")
        (dolist (datum (reverse data))
          (format output "~{~a~^,~}~%" datum))))))

#|           O:premises          1:task            2:             3: 
             rule                 cards            actual-freq    fn 
; (run-problem '(((A OR B) (A AND B)) POSSIBLE?          82       M-DELIBERATION) :verbose nil :parameters nil) => YES 
   (run-problem  '((if p then q)    ((p)(-p)(q)(- q)) 35           selection)) => ((P)(- Q)) 
  Call to (selection cards rule) |#
(defun run-problem (problem &key (verbose nil) (parameters nil))
  (reset-tracer)
  (when parameters
      (setf *converse*          (nth 0 parameters)
            *examine-all-cards* (nth 1 parameters)
            *falsification*     (nth 2 parameters)))
  (when verbose
    (format t "converse = ~A examine-all-cards = ~A falsification = ~A~%" *converse* *examine-all-cards* *falsification*))

  (let* ((rule (nth 0 problem))
         (cards (nth 1 problem))
         (fn (nth 3 problem)))
    (funcall fn cards rule)))

; (run-problem  '((if p then q)    ((p)(-p)(q)(- q)) 35           selection))
(defparameter *jlwason-1972* '(
    ((if p then q) ((p)(- p)(q)(- q)) 59 selection)))

; Example of problem from mSentential
(defparameter *hinterecker-et-al-2016-exp1*
  '( ( ((A or B) (A and B))  possible?   82 intuition )
    (((A ore B) (A and B)) possible?   10 intuition)
    (((A ore B) (A or B))  it-follows? 3  intuition)
    (((A or B) (A ore B))  it-follows? 24 intuition)))


;----------------------------------------------------------------------------------------------------------------------------
;                                               SYSTEM 0: LANGUAGE
;----------------------------------------------------------------------------------------------------------------------------

;--------------------------------
; Part 0.1 LEXICON AND GRAMMAR
;--------------------------------

#| word, syntactic category, and semantic fn, which is nil for syncategorematic words |#
(defparameter *lexicon* '(
   ((and)      (conn    (and-ing)))       
   ((or)       (conn    (or-psy)))  ;  inclusive
   ((ore)      (conn    (or-e)))    ;  exclusive
   ((unless)   (conn    (or-e)))
   ((if)       (c-antec (if-psy)))  
   ((iff)      (c-antec (if-f)))
   ((then)     (co       nil))      
   ((not)      (neg     (negate)))               
   ((comma)    (PUNCT    nil))     
   ((tautology)(PUNCT    nil)) ))

#| An unambiguous context-free grammar: expansion, non-terminal, compositional semantic fn. Different semantic 
functions for atomic sentences and for variables so that generation of descriptions works properly |#
(defparameter *grammar* '(
   ((var)                                (sentence (sem-aff-var)))
   ((neg var)                            (sentence (sem-neg-var)))
   ((sentence conn sentence)             (sentence (sem-scs) ))
   ((c-antec sentence co sentence)       (sentence (sem-cscs)))
   ((punct sentence conn sentence)       (sentence (sem-scs)))
   ((punct c-antec sentence co sentence) (sentence (sem-cscs)))
   ((neg sentence)                       (sentence (sem-negate)))))

(defvar *system* 1) ; global for Intuition (system 1) or Deliberation (system 2) in reasoning

;----------------------------------
; Part  0.2: The bottom-up parser
;----------------------------------

#| The BU Parser assumes an unambiguous grammar and closes off constituents as soon as possible, e.g. it returns, 
in effect,the following for:
   If a then b and c => ((if a then b) and c)  
But, punctuation can capture the other structure:
   If a then comma b and c => (if a then (b and c))
the word "comma" works as a left parenthesis, and all conectives take just two arguments. |#

#| comp-resul applies semantic fn of item about to go on p-stack to the unreduced p-stack. Update puts result 
into the right slot of the now syntactically revised p-stack |#
(defun parse (sentence)
  "shift and reduce parser that assumes unambiguous grammar. Semantics is sensitive to *system* 1 vs 2"
  (prog (p-stack new-stack)
    loop
    (cond((setf new-stack (reduces p-stack nil *grammar*)) ;nil for initial outlis
              (setf p-stack (update new-stack (comp-resul new-stack p-stack)))
              (go loop))
         ((null sentence)
              (cond((or (null p-stack)(cdr p-stack))
                        (print '(parse incomplete))(return nil))
                   (t  (return (cadar p-stack)))))
         ((setf p-stack (append p-stack (shift (car sentence) *lexicon*)))
                   (setf sentence (cdr sentence))
                   (go loop))
         (t (return '(error in parse))))))

(defun shift (word lex)
  "shifts word in lexicon, otherwise calls checkvar to treat word as a variable"
  (let ((rule (car lex)))
    (cond((null lex)(checkvar word))
         ((equal word (word_in rule))(category-&-semantics_in rule))
         (t (shift word (cdr lex))))))

(defun word_in(rule)
  (caar rule))

(defun category-&-semantics_in(rule)
  (cdr rule))

(defun checkvar(word)
  "if word not in lexicon, it is treated as a variable"
  (list (append (list 'var)(list(list word)))))

(defun reduces (inlis outlis gram)
  "reduces p-stack a/c to grammar - mapcar deletes semantics from p-stack before search in grammar"
  (let (item)
    (cond((null inlis) nil)
         ((setf item (red (mapcar #'car inlis) gram)) ;e.g. item is (NP1 (NPCODE))
            (append outlis (list item)))
         (t  (reduces (cdr inlis) (append outlis (list (car inlis))) gram)))))

(defun red(lis gram)
  "reduce calls this fn to compare p-stack with rhs of rules in grammar"
  (dolist (rule gram)
    (if (equal lis (expansion_of rule))
        (return (nonterminal_of rule)))))

(defun expansion_of(rule)
  (car rule))

(defun nonterminal_of(rule)
  (cadr rule))

(defun update (p-stack resul)
  "shifts word in lexicon, otherwise calls checkvar to treat word as a variable"
  (reverse(cons (append(cdr(reverse(car(reverse p-stack)))) resul)
              (cdr (reverse p-stack)))))

;----------------------------------------
; Part 0.3: The compositional semantics
;----------------------------------------

#|   new-stack = ((SENTENCE (SEM-CSCS))) 
     p-stack   = ((C-ANTEC (IF-I)) (SENTENCE (((A1) (B1)))) (CO NIL) (SENTENCE (((C1)))))
So, applies SEM-CSCS to p-stack, which retrieves #'IF-I, and applies it to the two sets of models
((A1)(B1)) and (((C1))) => ((((A) (B) (C)) ((T0)))) |#
(defun comp-resul(new-stack p-stack)
  "retrieves semantic_fn from new-stack and applies it ot p-stack"
  (list (apply (semantic-fn_on new-stack)(list p-stack))))

(defun semantic-fn_on(stack)
  (caadar (reverse stack)))

(defun sem-scs (stak)
  "composes semantics for s connectivve s"
  (let ((connective (car(cadadr (reverse stak))))
        (models1 (cadr(caddr(reverse stak))))
        (models2 (cadar (reverse stak))))
    (funcall connective models1 models2)))

(defun sem-cscs(stak)
  "composes semantics for c-antec s connective s for if_then"
  (let ((connective (caadr (cadddr(reverse stak))))
        (models1 (cadr(caddr(reverse stak))))
        (models2 (cadar (reverse stak))))
    (funcall connective models1 models2)))

(defun sem-negate(stak)
  "negates a set of models in order to do sentential negation"
  (negate (cadar (reverse stak))))
 
(defun sem-aff-var(stak)
  "semantics for for variables to get proper generation by gen-sen" 
  (list (list (upfun stak))))

(defun sem-neg-var(stak)
  "sem-neg for variables to get proper generation by gen-sen"
  (list(list(negate(upfun stak)))))

(defun upfun (stak)
  "rtns the semantic-fn in the last item on stak"
  (cadar(reverse stak)))

;-----------------------------------------------------------------------------------------------------------
; Part 0.4: Negation
;-----------------------------------------------------------------------------------------------------------

(defun negate (models)
  "rtns complement of a set of models (not psychologically realistic)"
  (cond((truth-valuep models)(not models))
       ((atom (car models))(neg models))
       ((listp (car models))
           (setf models (flesh-out(make-explicit models)))     ; with implicit
           (comp models (allpos (findatms models)))))) 
     
(defun truth-valuep(models)
  "Rtns t iff models are t or nil"
  (or (eq models t)(eq models nil)))
 
(defun neg (item)
  "puts '- in front of symbol, or removes it if already there"
  (if (equal (car item) '-)
      (cdr item)
     (cons '- item))) 

;---------------------------------------------------------------------------------------
; Part 0.5: Lexical semantics for 'and', 'if', 'iff', and 'or' (inclusive and exclusive)
;---------------------------------------------------------------------------------------

(defun and-ing (models1 models2)
  "ands two sets of models, calling either Intuition (system 1) or Deliberation (system 2)" 
  (setf models1 (eval-simple-var models1) models2 (eval-simple-var models2)) 
  (cond((or (null models1)(null models2)) nil)           ; both systems
       ((eq models1 t) models2)                          ; "
       ((eq models2 t) models1)                          ; "
       ((= *system* 1) (and-lis #'and-system-1 models1 models2))
       ((= *system* 2) (flesh-out(make-explicit(and-lis #'and-system-2 models1 models2))))
       (t (error "Unrecognized value of *system* variable"))))

(defun and-lis (fun models1 models2)
  "applies fn to every pair of models from two sets of models"
  (let ((mods1 models1)(mods2 models2) output)
  (dolist (mod1 mods1 output)
    (dolist (mod2 mods2)
      ; (setf output (append output (apply fun (list mod1 mod2))))))))
       (setf output (append output (apply fun (list mod1 mod2 models1 models2))))))))

(defun and-system-1 (mod1 mod2 &optional models1 models2)
  "conjoins two models from different sets of models, based on conjoin in mSentential"
  (cond((wholly-implicit mod1)
           (if (wholly-implicit mod2) 
               (list mod1)
             (impl-x-expl mod2 mod1 models1)))
       ((wholly-implicit mod2)(impl-x-expl mod1 mod2 models2))
       (t (and-explicit mod1 mod2))))

(defun and-system-2(mod1 mod2 &optional models1 models2)
  "ands models, which may be wholly or partly implicit, to rtn fems"
  (let* ((exps1 (explicit-part mod1))(imps1 (includes-implicit mod1))   
         (exps2 (explicit-part mod2))(imps2 (includes-implicit mod2))
         (expout (output exps1 exps2 imps1 imps2))
         (impout (output (eval imps1)(eval imps2) exps1 exps2))
         (finout (final-exp-models expout impout exps1 exps2 imps1 imps2)))
  (part-imp-output expout finout))) 

(defun output(exps1 exps2 imps1 imps2)
  "applies and-explicit to explicit models"
  (cond( exps1 
         (cond( exps2 (and-lis #'and-explicit exps1 exps2))
              ( imps2 exps1)))
       ( imps1 
         (cond( exps2 exps2)))))

(defun final-exp-models(expout impout exps1 exps2 imps1 imps2)
  "combines explicit output with implicit output => explicit models, or nil if contradiction "
  (cond( expout
         (cond( impout (and-lis #'and-explicit expout impout))   
              ((and imps1 imps2) nil)  
              (t expout)))
       ((and exps1 exps2) nil)    
       (impout impout)))

(defun part-imp-output(expout finout)
  "computes final footnote, subtracting expout from finput to yield one or disjunction of entries"
  (let ((imp-inf nil)(anonymous nil))
    (cond((setf imp-inf (rem-itms-from-models (car expout) finout))
              (setf anonymous (gentemp))
              (set anonymous imp-inf)
              (list (append-mods (car expout)(car (modelize anonymous)))))
         (t finout))))

(defun rem-itms-from-models(mod1 models2)
  "removes each item in mod1 from each model in models, using rem-mod1-from-mod2"
  (apply #'append                  
         (mapcar #'(lambda(md) 
                     (cond((setf md (rem-mod1-from-mod2 mod1 md))(list md)))) 
                 models2)))                                                  

(defun rem-mod1-from-mod2(mod1 mod2)
  "removes each item in mod1 from mod2"
  (if (null mod1) 
      mod2
    (rem-mod1-from-mod2 (cdr mod1)(rem-atom (car mod1) mod2))))

(defun rem-atom (atom model)
  "remove atom from a model"
  (cond ((null model) nil)
        ((equal atom (car model)) (cdr model))
        (t (cons (car model) (rem-atom atom (cdr model))))))

(defun and-explicit(mod1 mod2 &optional models1 models2)
  "joins two fems, doesn't rtn nil in case join-explicits rtns nil"
  (let ((outmods nil))
    (append models1 models2)    ; dummy function
    (if (setf outmods (join-explicits mod1 mod2))
        (list outmods))))

(defun join-explicits(mod1 mod2)
  "joins two fems without redundancy, rtning nil if one has item negating itm in other"
  (let (output)
    (dolist(m1 mod1 output)
      (cond((match m1 mod2)(setf output (append output (list m1)) mod2 (remove-itm m1 mod2)))
           ((match (negate m1) mod2)(return (setf output nil)))
           (t (setf output (append output (list m1))))))
    (if output (append output mod2))))

(defun impl-x-expl (expl-mod impl-mod other-mods-imply)
  "conjoins an explicit model with an implicit one, taking into account other models of which latter is a member"
  (if (common-members expl-mod other-mods-imply)
      nil
    (list (append expl-mod impl-mod))))

(defun common-members(mod models)
  "rtns all atoms in mod that are common to set of models, from mSentential"
  (let ((item nil))
    (cond((null mod) nil)
         ((setf item (match-itm-mod (car mod) models))
             (cons item (common-members (cdr mod) models)))
         (t  (common-members (cdr mod) models)))))

(defun match-itm-mod(item models)
  "checks whether itm occurs in any model in models"
  (cond((null models) nil)
       ((match item (car models)) item)
       (t (match-itm-mod item (cdr models)))))

(defun if-psy (models1 models2)
  (let ((anonymous (gentemp))) ; variable for implicit models
    (set anonymous (negate models1))
    (if (null (eval anonymous))
        (and-ing models1 models2)
    (append-models (and-ing models1 models2)(modelize anonymous)))))

(defun if-f (models1 models2)
  "biconditional interpretation"
  (let ((anonymous (gentemp))) ; variable for implicit models
    (set anonymous (and-ing (negate models1)(negate models2)))
    (if (null (eval anonymous))
        (and-ing models1 models2)
      (append-models (and-ing models1 models2)(modelize anonymous)))))

(defun or-e(models1 models2)
  "exclusive disjunction"
  (let ((anon1 (gentemp))(anon2 (gentemp)))
    (set anon1 (negate models1))
    (set anon2 (negate models2))
    (append-models (and-ing models1 (modelize anon2))
                   (and-ing models2 (modelize anon1)))))

(defun or-psy(models1 models2)
  "inclusive disjunction"
  (let ((anon1 (gentemp))(anon2 (gentemp)))
    (set anon1 (negate models1))
    (set anon2 (negate models2))
    (append-models   (and-ing models1 (modelize anon2))
                     (append-models (and-ing models2 (modelize anon1))
                                    (and-ing models1 models2)))))

(defun append-models(models1 models2)
  "appends models, making them fully expicit for Deliberation"
(cond((= *system* 1)(append-mods models1 models2))
     ((= *system* 2)(flesh-out(make-explicit(append-mods models1 models2))))))

(defun append-mods(models1 models2)
  "makes single set of models from two sets"
  (cond((eq models1 t)
         (cond((eq models2 t) t)
              ((eq models2 nil) t)
              (t (append (list t) models2))))
     ((eq models2 t)(append models1 (list t)))
     (t (append models1 models2))))

(defun modelize(var)
  "for sys 1, turns variable into set of models; for sys 2 evaluates the variable"
  (list(list(list var))))

;----------------------------------------
; Part 2.2:  Make models fully explicit
;----------------------------------------

(defun flesh-out (models)
  "fleshes out explicit models from make explicit, e.g, (((a)(b))(- a)) => fem of conditional"
  (if (truth-valuep models) 
      models
     (let* ((template (findatms models))(templ template))
       (dolist(itm templ)
         (setf models (flesh itm models)))
       (re-arranges template (tidy-up models)))))

(defun findatms (mods &optional lis)
  "rtns a list of each atom, once only, in the order that they occur in mods, treatingatm and its negation as same"
  (if (null mods) 
      (reverse lis)
    (findatms (cdr mods) (append (fi-atms (car mods) lis)))))

(defun fi-atms(mod lis)
  "rtns literals in mod with those in lis, and rtns each once only"
  (cond((null mod) lis)
       ((or (match (car mod) lis)
            (match (negate (car mod)) lis)) (fi-atms (cdr mod) lis))
       (t (fi-atms (cdr mod) (cons (car mod) lis)))))

(defun tidy-up(models)
  "puts models into standard order, and removes duplicates if nec, but not if their footnotes differ"
  (if (truth-valuep models) 
      models
     (imp-to-end (re-arranging (remove-dups models)))))

(defun imp-to-end(models)
  "puts wholly-implicit models at the end of the models"
  (cond((null models) nil)
       ((wholly-implicit (car models))(append (imp-to-end (cdr models))(list (car models))))
       (t (cons (car models)(imp-to-end (cdr models))))))

(defun re-arranging(models)
  "puts each model into same order as template from findatms"
  (let ((template (findatms models)))
    (re-arranges template models)))

(defun re-arranges(template models)
  "puts each model into the same order as the template"
  (cond((null models) nil)
       ((wholly-implicit (car models))(cons (car models)(re-arranges template (cdr models))))
       (t (cons (re-arr template (car models))(re-arranges template (cdr models))))))

(defun re-arr(template mod)
  "puts items in a model in same order as template"
  (let ((atm nil))
    (cond((null template) nil)
         ((setf atm (match-literal (car template) mod)) ; rtns atm corresponding to literal
            (cons atm (re-arr (cdr template)(remove-itm atm mod))))
         (t (re-arr (cdr template) mod)))))

(defun match-literal(lit mod)
  "rtns actual atom, neg or aff, in mod that matches lit"
  (cond((match lit mod) lit)
       ((match (negate lit) mod)(negate lit))))

(defun remove-dups (models)
  "eliminates duplicate tokes of models, but sensitive to different footnotes"
  (cond((null models) nil)  
       ((eq models t) t)
       ((matchmod (car models)(cdr models))(remove-dups (cdr models)))
       (t (cons (car models)(remove-dups (cdr models))))))

(defun matchmod(mod models)
  "rtns model from models if it matches mod, regardless of order of items, sensitive to negation"
  (cond((null models) nil)
       ((matchlists (car models) mod)(car models))
       (t (matchmod mod (cdr models)))))

(defun flesh(item models)
  "ok adds aff item and neg item to make separate models if neither is in a model"
  (let ((mod (car models)))
    (cond((null models) nil)
         ((or (match item mod)
              (match (neg item) mod))
                (cons mod(flesh item (cdr models))))
         (t (cons (cons item mod)
                (cons (cons (neg item) mod)(flesh item (cdr models))))))))

(defun make-explicit(models)
  "makes partly explicit and wholly explicit models explicit by adding their values, e.g., for conditional
     (((a)(b))(t1)) => (((a)(b))((- a))), and so needs fleshing out"
  (cond((null models) nil)
       ((explicit (car models))(cons (car models)(make-explicit (cdr models))))
       ((partly-implicit (car models))
          (append-mods (part-impl-to-expl (car models))(make-explicit (cdr models))))
       (t (append-mods (eval (wholly-implicit (car models)))(make-explicit (cdr models))))))

(defun part-impl-to-expl(model)
  "makes variable in partly-explicit model into set of fems"
  (let ((imp-mods (eval (partly-implicit model)))
        (exp-mods (list (remove-implicit model))))
    (cond((eq imp-mods t) exp-mods)
         ((eq exp-mods t) imp-mods)
         ((or (eq imp-mods nil)(eq exp-mods nil)) nil)
         (t  (and-lis 'and-explicit exp-mods imp-mods)))))

(defun remove-implicit(model)
  "from mSententialreason removes footnotes from an otherwise explicit model"
  (let (outmodel)
  (dolist(lit model outmodel)
    (if (not (footnotep lit))
        (setf outmodel (append outmodel (list lit)))))))

(defun footnotep(literal)
  (boundp (car (last literal))))

(defun explicit(model)
  "t iff model is wholly explicit"
  (not(includes-implicit model)))


(defun explicit-part(mod)
  "rtns explicit-part of model"
  (if (setf mod (explic-part mod))
      (list mod)))

(defun explic-part(mod)
  "recurses to rtn explicit part"
  (if (or (null mod)(boundp(car(reverse(car mod)))))
      nil
    (cons (car mod)(explic-part (cdr mod)))))

(defun wholly-implicit(model)
  "rtns variable from wholly implicit model"
  (if (= (length model) 1)
      (includes-implicit model)))

(defun partly-implicit(model)
  "if model is partly implicit rtns variable"
  (if (> (length model) 1)
      (includes-implicit model)))

(defun includes-implicit(model)
  "rtns variable if model is partly or wholly implicit"
  (let ((item nil))
    (cond((null model) nil)
         ((and (setf item (car(reverse(car model))))(boundp item))
             item)
         (t  (includes-implicit (cdr model))))))

(defun eval-simple-var(models)
  "where a set of models contains only a wholly implicit model, rtns its truth value if it has one"  
  (let ((var nil))
    (cond((eq models t) models) ; otherwise error in only-imp-mod for t
         ((and (setf var (only-imp-mod models))(truth-valuep (eval var)))
                 (eval var))                         
         (t models))))

(defun only-imp-mod(models)
  "if models contains only a single model that is wholly implicit rtns its variable"
  (and (= (length models) 1)(wholly-implicit (car models))))

(defun member-lis(itm lists)
  (dolist (lis lists)
    (if (equal itm lis)(return lis))))

(defun comp(models allposmodels)
  "removes each member of models from allposmodels
   (comp '(((a)(b))((- a)(- b))) '(((a)(b))((a)(- b))((- a)(b))((- a)(- b)))) => (((a)(- b))((- a)(b)))"
  (dolist(mod models)
    (if (null models)
        allposmodels
    (setf allposmodels (remove-itm mod allposmodels))))
  allposmodels)

#|
negate
  truth-valuep
  neg
  flesh-out
  make-explicit
  comp
  allpos
  findatms
(defun negate (models)
  "rtns complement of a set of models (not psychologically realistic)"
  (cond((truth-valuep models)(not models))
       ((atom (car models))(neg models))
       ((listp (car models))
           (setf models (flesh-out(make-explicit models)))     ; with implicit
           (comp models (allpos (findatms models)))))) |#

(defun remove-itm (itm lis)
  (cond((null lis) nil)
       ((matchlists itm (car lis))(remove-itm itm (cdr lis)))
       (t (cons (car lis) (remove-itm itm (cdr lis))))))

(defun matchlists (lis1 lis2)
  "rtns lis2 iff it and lis1 have identical members,e.g. ((a)(b)) = ((b)(a))"
  (cond((equal lis1 lis2) lis2)
       ((null lis1) nil)
       ((and (matchl lis1 lis2)(matchl lis2 lis1)) lis2)))

(defun matchl (lis1 lis2)
  "rtns t iff each item in lis1 is in lis2 and vice versa"
  (cond((null lis1) t)
       ((match (car lis1) lis2)(matchl (cdr lis1) lis2))))

(defun match (item mod)
  "rtns item (or mod) iff it occurs in mod (or lis in same order), sensitive to polarity"
  (cond((null mod) nil)
       ((equal item (car mod))(car mod))
       (t (match item (cdr mod)))))

(defun allpos (lst1 &optional lst2)
  "ok generates all possible contingencies from a list of literals"
  (if (null lst2)
      (setf lst2 '(())))
  (cond((null lst1) nil)
       ((null (cdr lst1))
          (flesh (car lst1) lst2))
     (t (flesh (car lst1)(allpos (cdr lst1) lst2)))))

;;;;; END OF FILE


