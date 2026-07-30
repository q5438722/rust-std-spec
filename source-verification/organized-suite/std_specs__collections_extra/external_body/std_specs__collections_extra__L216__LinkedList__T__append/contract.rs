pub assume_specification<T>[ LinkedList::<T>::append ](
    list: &mut LinkedList<T>,
    other: &mut LinkedList<T>,
)
    ensures
        final(list)@ == old(list)@ + old(other)@,
        final(other)@ == Seq::<T>::empty(),
;
