# Imports
from typing import List


class Run:

    def __init__(
            self,
            user: str = "",
            soft: List[str] = None
    ) -> None:
        """
        Init instance of Run class.

        This class configure privates arguments `__user` and `__soft`.
        - `__user` contains the type of client using the script
        - `__soft` contains the software to install on machine
        If a list is provided, it is copied to avoid side effects related
        to external references.
        Otherwise, an empty list is created.

        Args:
            user (str, optional): type of user SERVER or CLIENT.
                Default value : "".
            soft (List[str], optional): Default list of the software.
                Default value : None.

        Attributes:
            __user (str): type of user SERVER or CLIENT (private).
            __soft (List[str]): List installation software (private).

        Examples:
            run = Run(user="CLIENT", soft=["Docker", "PostgreSQL"])
        """
        self.__soft: List[str] = soft.copy() if soft else []
        self.__user: str = user

    @property
    def soft(
        self
    ) -> List[str]:
        """
        Returns a copy of the list of software associated with the user.

        Returns:
            List[str]: A copy of the user's software list.

        Examples:
            run = Run(user="CLIENT", soft=["Docker", "PostgreSQL"])
            run.soft
            ['Docker', 'PostgreSQL']
        """
        return self.__soft.copy()

    @soft.setter
    def soft(
        self,
        soft: str
    ) -> None:
        """
        Adds a software item to the user's software list.

        Args:
            soft_item (str): Name of the software to add.

        Raises:
            TypeError: If soft_item is not a string.

        Examples:
            run = Run()
            run.soft = "Docker"
        """
        if not isinstance(soft, str):
            raise TypeError("Params : soft is not a string")
        self.__soft.append(soft)

    @property
    def user(
        self
    ) -> str:
        """
        Returns the user's name or identifier.

        Returns:
            str: The user's name or type.

        Examples:
            run = Run(user="CLIENT")
            run.user
            'CLIENT'
        """
        return self.__user

    @user.setter
    def user(
        self,
        user: str
    ) -> None:
        """
        Sets the user's name or identifier.

        Args:
            user (str): Name or type of the user.

        Raises:
            TypeError: If user is not a string.

        Examples:
            run = Run()
            run.user = "SERVER"
        """
        if not isinstance(user, str):
            raise TypeError("Params : user is not a string")
        self.__user = user

    def multi_soft(
        self,
        *softs: str
    ) -> None:
        """
        Adds multiple software items to the user's software list.

        Args:
            *softs (str): One or more software names to add.

        Raises:
            TypeError: If any element in softs is not a string.

        Examples:
            run = Run()
            run.multi_soft("Docker", "PostgreSQL")
        """
        for soft in softs:
            if not isinstance(soft, str):
                raise TypeError("Params : soft is not a string")
            self.__soft.append(soft)

    def __repr__(
        self
    ) -> str:
        """
        Returns a readable string representation of the Run object.

        Returns:
            str: A string showing the user and the software list.

        Examples:
            run = Run(user="CLIENT", soft=["Docker"])
            repr(run)
            "Run(user='CLIENT', soft=['Docker'])"
        """
        return f"Run(user={self.__user!r}, soft={self.__soft!r})"
