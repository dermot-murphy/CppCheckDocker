/* Deliberate MISRA C:2012 violation for CppCheckDocker test suite.
 * Rule 15.1 (advisory): The goto statement should not be used.
 */
int main(void)
{
    goto end;
end:
    return 0;
}
