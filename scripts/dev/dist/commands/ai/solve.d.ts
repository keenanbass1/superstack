interface SolveOptions {
    model: string;
    context: boolean;
}
export declare function solve(problem: string, options: SolveOptions): Promise<void>;
export {};
